import ssl

# Function to initialize SSL context for secure client-server communication
def setup_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile="certs/server.crt")  # Load the server certificate for verification
    return context
