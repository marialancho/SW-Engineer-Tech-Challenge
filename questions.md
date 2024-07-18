# Floy Technical Challenge

## Questions

**1. What were the reasons for your choice of API/protocol/architectural style used for the client-server communication?**

**API:**
I chose FastAPI for building the server-side API. I chose it because it is modern and fast, and has web framework capabilities for building APIs with Python 3.7+ based on standard Python type hints. It also has automatic interactive API documentation that makes it easy to develop and test. Besides, it supports asynchronous programming, which is crucial for handling multiple input/output operations efficiently.

**Protocol:**
HTTP/REST was chosen as the communication protocol. HTTP is a well-established protocol widely used in web applications. REST is an architectural style that uses standard HTTP methods (GET, POST, PUT, DELETE) for CRUD operations. It is stateless, which simplifies server design and scales well across multiple clients.

**Architectural Style:**
The architectural style used is a client-server model. This model separates the client (which sends requests) from the server (which processes requests and sends responses). This separation allows for independent development, maintenance, and scaling of client and server components. The client handles receiving DICOM files and sending the extracted information to the server, while the server is responsible for processing, storing, and providing access to the data via RESTful endpoints.







**2.  As the client and server communicate over the internet in the real world, what measures would you take to secure the data transmission and how would you implement them?**

To secure data transmission over the internet, I would implement different measures:

**HTTPS:**
Encrypt data in transit using SSL/TLS certificates, ensuring confidentiality and integrity. This can be achieved by configuring the server to use HTTPS.
To implement this, an SSL certificate can be obtained from a Certificate Authority and the FastAPI serer can be configured to use it.

**Authentication:**
API keys can be used to authenticate clients and ensure that only authorized users can access the API. The API keys can be easily implemented in FastAPI.


**Access Control:**
Implement role-based access control to manage permissions and restrict access to sensitive data. For example by defining roles and permissions in the application and checking them before allowing access to endpoints.


**Regular Updates:**
Keep the server, dependencies, and libraries updated to protect against known vulnerabilities by regularly checking for updates to Python packages and the FastAPI framework and applying them.


**Secure Storage:**
Encrypt sensitive data within the database to prevent unauthorized access if the storage medium is compromised.  This could be implemented with the library sqlcipher, since we have a SLite database.
