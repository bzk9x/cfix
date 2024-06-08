### `.cfix` File Format:

The `.cfix` file format is a custom file format utilized by the Cfix application to encapsulate and store contact information efficiently. It is designed to include all relevant details about a contact, including their name, phone number, email, profile image, and metadata. Below is a detailed breakdown of the structure and components of a `.cfix` file:

#### JSON Format:
A `.cfix` file is formatted using JSON, a lightweight data interchange format. 
#### Components

1. **Contact Information**:
   - **Name**: The contact's name.
   - **Phone Number**: The contact's phone number.
   - **Email**: The contact's email address.

2. **Profile Image**:
   - The profile image is stored as a base64 encoded string within the `.cfix` file. Base64 encoding converts binary data (such as an image) into ASCII characters, allowing it to be represented as text. This ensures that the image data can be embedded directly into the JSON structure.

3. **Metadata**:
   - Additional information about the contact is stored in the metadata section. This typically includes:
     - **Creation Timestamp**: The date and time when the contact was created.
     - Other metadata fields can be added as needed, such as the last modified timestamp or any custom attributes relevant to the application.

#### Example `.cfix` File:

```json
{
    "name": "John Doe",
    "phone_number": "+1234567890",
    "email": "johndoe@example.com",
    "profile_image": "/9j/4AAQSkZJRgABAQEAAAAAAAD/...",
    "metadata": {
        "created_at": "2023-06-08 14:55:00"
    }
}
```

#### Explanation of Components:

- **Name**: The contact's name, such as "John Doe".
- **Phone Number**: The contact's phone number, in a standardized format (e.g., "+1234567890").
- **Email**: The contact's email address, such as "johndoe@example.com".
- **Profile Image**: The profile image of the contact, encoded as a base64 string. This string represents the binary data of the image in a text format.
- **Metadata**: Additional information about the contact, stored as key-value pairs. In this example, the `created_at` field indicates when the contact was created, represented as a timestamp.
