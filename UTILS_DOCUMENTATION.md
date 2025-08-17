# File Processing Utils - Usage Examples

This document provides examples of how to use the `utils.py` module for file processing.

## Quick Start

```python
from utils import process_uploaded_file, format_file_size, get_supported_file_types

# Process an uploaded file (in Streamlit context)
if uploaded_file is not None:
    content, file_details = process_uploaded_file(uploaded_file)
    
    # Display file information
    st.write(f"**File Name:** {file_details['filename']}")
    st.write(f"**File Type:** {file_details['filetype']}")
    st.write(f"**File Size:** {format_file_size(file_details['filesize'])}")
    
    # Display processed content
    if isinstance(content, str):
        st.text_area("File Content", content, height=300)
    else:  # For images
        st.image(content, caption=file_details['filename'])
```

## Available Functions

### Core Processing Functions
- `process_uploaded_file(uploaded_file)` - Main function to process any supported file type
- `upload_to_gemini(file_content, file_details)` - Prepare content for Gemini AI processing

### Utility Functions
- `format_file_size(size_bytes)` - Convert bytes to human-readable format
- `get_supported_file_types()` - Get dictionary of supported file types
- `is_supported_file_type(file_type)` - Check if a file type is supported

### FileProcessor Class Methods
- `FileProcessor.process_text_file(uploaded_file)` - Process .txt files
- `FileProcessor.process_pdf_file(uploaded_file)` - Process .pdf files  
- `FileProcessor.process_word_file(uploaded_file)` - Process .docx files
- `FileProcessor.process_excel_file(uploaded_file)` - Process .xlsx/.xls files
- `FileProcessor.process_csv_file(uploaded_file)` - Process .csv files
- `FileProcessor.process_json_file(uploaded_file)` - Process .json files
- `FileProcessor.process_image_file(uploaded_file)` - Process image files

## Supported File Types

| Extension | MIME Type | Processing Features |
|-----------|-----------|-------------------|
| .txt | text/plain | Full text extraction |
| .pdf | application/pdf | Page-by-page text extraction |
| .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document | Paragraphs + tables |
| .xlsx/.xls | application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | Multi-sheet analysis, statistics |
| .csv | text/csv | Data analysis, missing values, statistics |
| .json | application/json | Structure analysis, pretty formatting |
| .jpg/.png/.gif | image/jpeg, image/png, image/gif | Image metadata, AI-ready format |

## Error Handling

All functions include comprehensive error handling and return helpful error messages:

```python
content, file_details = process_uploaded_file(uploaded_file)

if content.startswith("Error"):
    st.error(f"Failed to process file: {content}")
else:
    # Process successful content
    pass
```
