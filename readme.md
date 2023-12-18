# Trash Can Client API Documentation
This documentation provides a comprehensive guide to the Trash Can Client API, a Flask-based web service designed to manage and retrieve trash collection data.

## Overview
The Trash Can Client API interacts with the MijnAfvalWijzer API to fetch and manage trash collection data. It uses MongoDB for data storage and provides endpoints for retrieving collection data and managing stored data.

## Setup and Running
Before running the API, ensure that the required environment variables are set, including the MIJN_AFVAL_WIJZER_API_KEY for the external API and MongoDB settings. Use the load_dotenv function to load variables from a .env file.

To run the API:

```python
if __name__ == '__main__':
    app.run(
        port=flask_client.get_port(),
        debug=flask_client.get_debug(),
        host=flask_client.get_host()
    )
```
## Endpoints
### GET /
- Retrieves collection data based on the provided address details.
- Input: JSON object with zip_code, house_number, and add_on.
- Output: A list of collection data for the given address.
- Error Handling: Returns a 422 status code with error messages in case of invalid input.
### DELETE /
- Deletes all the collections from the database.
- Output: Confirmation message on successful cleanup.
- Error Handling: Returns a 404 status code if collections are not found. 
- ###DELETE /<key>
- Deletes a specific collection identified by the key.
- Input: A key in the URL representing the collection to be deleted.
- Output: Confirmation message on successful cleanup of the specified collection.
- Error Handling: Returns a 404 status code if the specified collection is not found.
## Client Classes
### FlaskClient
Handles the configuration and setup of the Flask app.

### TrashCanClient
- Manages the interaction with the MijnAfvalWijzer API and MongoDB.
- Includes methods for data retrieval, cleanup, and date validation.
### Schema
## StreetSchema
Defines the schema for input validation using Marshmallow.

## Error Handling
The API uses ValidationError from Marshmallow for input validation and provides appropriate error messages and status codes.

## Additional Information
The API uses environment variables for configuration, including API keys and database settings.
MongoDB is used for storing and managing the collection data.
Ensure that the required Python packages are installed, use pip to install them
