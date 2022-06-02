## Importing Needed Packages

import ast
import pandas as pd 
import snowflake
import snowflake.connector
import re



## Connection Credentials

snow_Cred = {
    'user' : 'user',
    'password' : 'password',
    'account': 'account',
    'warehouse': 'warehouse',
    'database': 'database',
    'schema': 'schema'
}



### Main SQL connection and Query Functions

# Connects to the database to create a connection object "conn"
def snow_connect(snow_Cred):
    """ Connect to the Snowflake database server """
    conn = None
    try:
        # connect to the Snowflake server
        print('Connecting to the Snowflake database...')
        conn = snowflake.connector.connect(**snow_Cred)
        print('Connected to database')
    except (Exception, snowflake.connector.errors.ProgrammingError) as error:
        print(error)
        sys.exit(1) 
    return conn


# Executes a select SQL query and returns results in a Pandas DataFrame
def execute_select_query(pd_cur, sql_query):
    try:
        pd_cur.execute(sql_query)
        df = pd_cur.fetch_pandas_all()
    except (Exception, snowflake.connector.errors.ProgrammingError) as error:   
        print('SOME ERROR')
        print(error)
        sys.exit(1) 
    #finally:
    #    pd_cur.close()
    return df


# Executes an Update or Insert SQL query and returns results in a Pandas DataFrame
def execute_upsert_query(pd_cur, sql_query):
    try:
        pd_cur.execute(sql_query)
    except (Exception, snowflake.connector.errors.ProgrammingError) as error:   
        print('SOME ERROR')
        print(error)
        sys.exit(1) 
    #finally:
    #    pd_cur.close()
    return True


conn = snow_connect(snow_Cred)
pd_cur = conn.cursor()



### Main Query to get Transactions

mastercard_transaction = "SELECT LEFT(DATE_TRUNC(MONTH, mc_trans.AT), 10) AS expense_month, mc_trans.* FROM APP_MOONCARD_CO.PUBLIC.MASTERCARD_TRANSACTIONS mc_trans WHERE TO_DATE(AT) = TO_DATE(current_date) - 1 AND TRANSACTION_TYPE IN ('1') ORDER BY AT DESC LIMIT 200;"
mcrd_int_df = execute_select_query(pd_cur, mastercard_transaction)
#mcrd_int_df.head(3)



##  Insert calculated interchange

def insert_interchange(id, expense_month, expense_amount, expense_type, amount_cost, amount_base, amount_exchange, amount_fees):
    insrt_intr_chng = "INSERT INTO  APP_MOONCARD_CO.PUBLIC.MASTERCARD_INTERCHANGES_CALCULATED (ID, EXPENSE_MONTH, EXPENSE_AMOUNT, EXPENSE_TYPE, AMOUNT_COST, AMOUNT_BASE, AMOUNT_EXCHANGE, AMOUNT_FEES) VALUES ('{trans_id}', '{exp_month}', '{exp_amount}', '{exp_type}', '{amt_cost}', '{amt_base}', '{amt_exchange}', '{amt_fees}');".format(trans_id = id, exp_month = expense_month, exp_amount = expense_amount, exp_type = expense_type,  amt_cost = amount_cost, amt_base = amount_base, amt_exchange = amount_exchange, amt_fees = amount_fees)
    print(insrt_intr_chng)
    execute_upsert_query(pd_cur, insrt_intr_chng)

    
    
## Calculating PS interchange

def ps_interchange_calculation(df_trans_slice): 
    sign = -1
    share_percent  = 0.00
    data = ast.literal_eval(df_trans_slice.DATA)
    expense_type = 0
    amount_cost = 0
    amount_exchange = 0
    expense_month = df_trans_slice.EXPENSE_MONTH
    id = df_trans_slice.ID

    if float(data['Bill_Amt']) > 0:
        sign = 1
        
    # Test for Online and Offline Transaction    
    if 'GPS_POS_Data' in data:   # Check Online or EMV Transaction of GPS_POS_Data  
        print(data['GPS_POS_Data'][2])
        if data['GPS_POS_Data'][2] in ('6', 'V', 'C', 'F', 'G'): # Online Transaction
            share_percent  = 0.0165
            
        elif data['GPS_POS_Data'][2] in ('5'): # EMV(Electromagnetic Validation) Transaction
            share_percent  = 0.0155
            
        
    elif 'POS_Data_DE22' in data: # Check Online or EMV Transaction of POS_Data_DE22  
        if bool(re.match("/^(81|01)[0-9]*$/", data['POS_Data_DE22'])): # Online Transaction
            share_percent  = 0.0165
            
        else: # check EMV(Electromagnetic Validation) Transaction
            chck_de22 = re.findall(r"/^\s*([0-9]{2})([0-9])\s*$/", data['POS_Data_DE22'])
            
            if len(chck_de22) > 0:
                if chck_de22[0] in (5, 6, 95): # EMV(Electromagnetic Validation) Transaction
                    share_percent  = 0.0155
                    
    else: # Transaction is OTHER
        val_seq = df_trans_slice.SEQUENCE
        scnd_select = "SELECT * FROM APP_MOONCARD_CO.PUBLIC.MASTERCARD_TRANSACTIONS WHERE SEQUENCE = '{param_val_seq}' AND TRANSACTION_TYPE = 1 AND TRANSACTION_STATUS = 1 ORDER BY AT ASC LIMIT 1;".format(param_val_seq = val_seq)
        scnd_mcrd_int_df = execute_select_query(pd_cur, scnd_select)
        
        scnd_data = ast.literal_eval(scnd_mcrd_int_df.DATA)

        
        if 'GPS_POS_Data' in scnd_data:   # Check Online or EMV Transaction of GPS_POS_Data  
            if scnd_data['GPS_POS_Data'][2] in ('5'): # EMV(Electromagnetic Validation) Transaction
                share_percent  = 0.0185
        
        elif 'POS_Data_DE22' in scnd_data:
            scnd_chck_de22 = re.findall(r"/^\s*([0-9]{2})([0-9])\s*$/", scnd_data['POS_Data_DE22'])
            if len(scnd_chck_de22) > 0:
                if scnd_chck_de22[0] in (5, 6, 95): # EMV(Electromagnetic Validation) Transaction
                    share_percent  = 0.0185
                
   
    total_fees = (abs(float(data['Fee_Fixed']))  + abs(float(data['Fee_Rate'])) ) * sign
    expense_amount = float(data['Bill_Amt'])  + total_fees
    amount_base =  -1 * (expense_amount * share_percent )
    
    
    if 'Txn_Ccy' in data: 
        if data['Txn_Ccy'] != 978:
            amount_exchange = -1 * (expense_amount - (expense_amount/(1 + 0.03)) )
    elif 'Txn_CCy' in data: 
        if data['Txn_CCy'] != 978:
            amount_exchange = -1 * (expense_amount - (expense_amount/(1 + 0.03)) )
    
    amount_fees = -1 * total_fees
    
    if amount_exchange > 0:
        amount_fees -=  amount_exchange
        
    expense_amount = round(expense_amount, 2)    
    if expense_amount == -0:
        expense_amount = 0
        
    amount_cost = round(amount_cost, 2)    
    if amount_cost == -0:
        amount_cost = 0
        
    amount_base = round(amount_base, 2)
    if amount_base == -0:
        amount_base = 0
        
    amount_exchange = round(amount_exchange, 2)   
    if amount_exchange == -0:
        amount_exchange = 0
        
    amount_fees = round(amount_fees, 2)
    if amount_fees == -0:
        amount_fees = 0
        
        
    print(id, expense_month, expense_amount, expense_type, amount_cost, amount_base, amount_exchange, amount_fees)
    #print("Ps Calculation", data['Bill_Amt'], 'sign ', str(sign),total_fees, amount_base, expense_amount, "id ", id)
    
    insert_interchange(id, expense_month, expense_amount, expense_type, amount_cost, amount_base, amount_exchange, amount_fees)
    
    
    
## calculation of AA / AI Interchange

def aa_interchange_calculation(df_trans_slice):
    data = ast.literal_eval(df_trans_slice.DATA)
    expense_type = 2
    amount_cost = -0.2
    amount_base = 0.0
    amount_exchange = 0
    amount_fees = 0.0
    expense_amount = 0.0
    expense_month = df_trans_slice.EXPENSE_MONTH
    id = df_trans_slice.ID
    
    if 'GPS_POS_Data' in data: # Check Online or EMV Transaction of GPS_POS_Data          
        if data['GPS_POS_Data'][3] in ('S'): # EMV(Electromagnetic Validation) Transaction            
            amount_cost -= 0.09
            
            
    expense_amount = round(expense_amount, 2)    
    if expense_amount == -0:
        expense_amount = 0
        
    amount_cost = round(amount_cost, 2)    
    if amount_cost == -0:
        amount_cost = 0
        
    amount_base = round(amount_base, 2)
    if amount_base == -0:
        amount_base = 0
        
    amount_exchange = round(amount_exchange, 2)   
    if amount_exchange == -0:
        amount_exchange = 0
        
    amount_fees = round(amount_fees, 2)
    if amount_fees == -0:
        amount_fees = 0
            
    print(id, expense_month, expense_amount, expense_type, amount_cost, amount_base, amount_exchange, amount_fees)
    insert_interchange(id, expense_month, expense_amount, expense_type, amount_cost, amount_base, amount_exchange, amount_fees)
    
    


### Check type of transaction and call appropriate method

def check_transaction_type(df_trans_slice):    

    # Check if PS
    if df_trans_slice.TRANSACTION_TYPE in (16, 14, 5) and df_trans_slice.TRANSACTION_STATUS == 19: # Check if PS
        # Call PS Calculation method
        print("PS")
        print(df_trans_slice)
        return ps_interchange_calculation(df_trans_slice)
    
    
    # Check if AA
    if df_trans_slice.TRANSACTION_TYPE == 1 and df_trans_slice.TRANSACTION_STATUS == 1: # Check if AA
        # Call AA Calculation method
        print("AA")
        return aa_interchange_calculation(df_trans_slice)
    
    
    # Check if AI
    if df_trans_slice.TRANSACTION_TYPE == 1 and df_trans_slice.TRANSACTION_STATUS == 9: # Check if AI
        # Call AI Calculation method
        print("AI")
        return aa_interchange_calculation(df_trans_slice)
    
    print(' -->', df_trans_slice)



    
    
### Main Query to get Transactions

mastercard_transaction = "SELECT * FROM APP_MOONCARD_CO.PUBLIC.Data_for_interchange;"
mcrd_int_df = execute_select_query(pd_cur, mastercard_transaction)
#mcrd_int_df.head(3)

"""
i = 0
mcrd_int_df.iloc[i]

"""

# Method call check_transaction_type(df_trans_slice)

for i in range(0, len(mcrd_int_df)):
    print(i)
    check_transaction_type(mcrd_int_df.iloc[i])
    