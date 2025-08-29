from langchain_core.documents import Document


class PromptGenService:
    def __init__(self):
        pass
    def generatePrompt(self , input_query : str , documents: list[Document])->str:
        return self.__prepareContext__(input_query , documents)
    def __prepareContext__(self , input_query:str , documents : list[Document])->str:
        return f'''You are an expert SQL analyst. Your task is to write a SQL query based on a user's request.
                Here is the table schema you must use:
                CREATE TABLE wo.DUPLO_WORK_ORDER (
                WORK_ORDER_ID VARCHAR(50),
                ASSET_ID VARCHAR(50),
                WORKFLOW_CODE VARCHAR(100),
                WORK_ORDER_STATUS VARCHAR(100),
                DUE_DATE DATE,
                PRIORITY VARCHAR(5),
                CREATED_TIME DATE,
                CREATED_BY VARCHAR(100),
                LAST_MODIFIED_TIME DATE,
                LAST_MODIFIED_BY VARCHAR(300),
                WORK_ORDER_KEY VARCHAR(300),
                INTERNAL_WORK_ORDER_ID VARCHAR(50),
                DISTRIBUTION_NAME VARCHAR(300),
                DISTRIBUTION_STATUS VARCHAR(300),
                DISTRIBUTION_TYPE VARCHAR(300),
                OPERATIONAL_GROUP_NAME VARCHAR(300),
                ASSIGNEE_NAME VARCHAR(300),
                ASSIGNEE_IS_ACTIVE VARCHAR(300),
                JOB_TYPE VARCHAR(300),
                FACILITY VARCHAR(100),
                REGION_NAME VARCHAR(100),
                WORK_ORDER_LANGUAGE VARCHAR(300),
                DISTRIBUTION_OPERATIONAL_REGION_ID VARCHAR(300),
                FACILITY_OPERATIONAL_REGION_ID VARCHAR(300),
                OPERATIONAL_GRP_OPERATIONAL_REGION_ID VARCHAR(300),
                ADDITIONAL_SERVICE_ID VARCHAR(300),
                ADDITIONAL_SERVICE_NAME VARCHAR(300),
                ODS_UPDATE_DATE DATE,
                MD5_HASH VARCHAR(100),
                CONSTRAINT PK_WORK_ORDER PRIMARY KEY (WORK_ORDER_ID)
                );

                ***Column Descriptions:***
                * **WORK_ORDER_ID**: A unique identifier for each work order. Use this for specific lookups.
                * **ASSET_ID**: The ID of the physical asset (e.g., equipment, machinery) that the work order is for.
                * **WORKFLOW_CODE**: A code representing the process or sequence of steps for the work order.
                * **WORK_ORDER_STATUS**: The current state of the work order (e.g., 'In Progress', 'Completed', 'Canceled').
                * **DUE_DATE**: The date by which the work order must be completed.
                * **PRIORITY**: The urgency level of the work order (e.g., '0', '1', '2').
                * **CREATED_TIME**: The timestamp when the work order was created. Use this for queries related to creation date or time.
                * **CREATED_BY**: The person or system that created the work order.
                * **LAST_MODIFIED_TIME**: The last time the work order was changed.
                * **LAST_MODIFIED_BY**: The person or system that last modified the work order.
                * **DISTRIBUTION_NAME**: The name of the group or team the work order was assigned to.
                * **DISTRIBUTION_STATUS**: The status of the work order's distribution.
                * **DISTRIBUTION_TYPE**: The type of distribution for the work order.
                * **OPERATIONAL_GROUP_NAME**: The name of the operational group responsible for the work order.
                * **ASSIGNEE_NAME**: The name of the individual assigned to perform the work.
                * **ASSIGNEE_IS_ACTIVE**: Indicates if the assigned person is currently active.
                * **JOB_TYPE**: The type of job or task the work order represents.
                * **FACILITY**: The physical building or location where the work is to be performed.
                * **REGION_NAME**: The geographical region of the work order.
                * **WORK_ORDER_LANGUAGE**: The language the work order is written in.
                * **ADDITIONAL_SERVICE_NAME**: The name of any extra service related to the work order.
                * **ODS_UPDATE_DATE**: The date the record was last updated in the Operational Data Store.

                Please ensure your query uses only the columns and table name provided above. Do not include any additional information, explanations, or text in your response. The response must be only the SQL query itself.
                {'\n'.join([f' - {self.prep_doc(doc)}' for doc in documents])}

                User: user_query
                SQL:
        '''
    def __prepDocumentContext__(self , docuemnt:Document)->str:
        return (
            f"Example: {docuemnt.metadata['prompt']}\n"
            # f"Database Schema: {docuemnt.metadata['schema_context']}\n"
            f"Sql Query: {docuemnt.metadata['sql_query']}\n"
            # f"Domain: {docuemnt.metadata['domain']}\n"
        )
    def prep_doc(self , item:Document):
        return (
                f"Example: {item.metadata['prompt']}\n"
                # f"Database Schema: {item.metadata['schema_context']}\n"
                f"Sql Query: {item.metadata['sql_query']}\n"
                # f"Domain: {item.metadata['domain']}\n"
            )