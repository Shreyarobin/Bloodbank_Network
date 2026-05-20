import ssl

# Function to initialize SSL context for secure communication
def setup_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # Load the server's certificate and key from the certs folder
    context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")
    
    # Optionally disable older SSL versions for enhanced security
    context.options |= ssl.OP_NO_SSLv2
    
    return context
