import mariadb
class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mariadb.connect(**self.config)
            self.connection.autocommit = True  
            self.cursor = self.connection.cursor()
            return True
        except mariadb.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def get_next_sample_id(self):
        try:
            if not self.connection:
                if not self.connect():
                    return "BATCH_001"

            self.cursor.execute("SELECT MAX(Sample_ID) FROM FullBatch_tab")
            result = self.cursor.fetchone()[0]

            if result is None:
                return "BATCH_001"
            
            prefix = "BATCH_"
            num = int(result.replace(prefix, ""))
            next_id = f"{prefix}{num + 1:03d}"
            return next_id

        except Exception as e:
            print(f"Error generating next sample ID: {e}")
            return "BATCH_ERR"


    def save_batch(self, sample_id, nugget_count, batch_weight, batch_validity):
        try:
            if not self.connection:
                if not self.connect():
                    return False

            insert_query = """
            INSERT INTO Fullbatch_tab (Sample_ID, Nugget_Count, Batch_weight, Batch_validity)
            VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (str(sample_id), nugget_count, batch_weight, batch_validity))
            self.connection.commit()
            print(f"Rows affected: {self.cursor.rowcount}")
            return True
        except mariadb.Error as e:
            print(f"Error saving batch to database: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()