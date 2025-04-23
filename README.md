To run the project:

### 1. clone the repository
git clone https://github.com/rahulraj710/ReceiptProcessor.git

### 2. Navigate to the project folder
cd ReceiptProcessor

### 3. start the docker container
docker-compose up --build

The app will be available at:
http://localhost:8000/

### Endpoints
Method    Endpoint                            Description
POST	    /receipts/process	                  Submit a receipt
GET	      /receipts/<receipt_id>/points	      Get points for a given receipt
GET	      /swagger/	Interactive Swagger       API docs

### Testing
You can use swagger to test the end points:
http://localhost:8000/swagger


### Notes
The app stores receipt data in memory (no database). 
Data is lost when the server restarts.
