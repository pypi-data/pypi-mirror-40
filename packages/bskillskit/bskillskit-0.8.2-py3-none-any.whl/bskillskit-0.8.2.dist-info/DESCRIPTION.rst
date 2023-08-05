It is a helper tool with reference to box skills. It is not official.
This module refers to the box skill kit nodejs and the Box Python SDK.
https://github.com/box/box-skills-kit-nodejs
https://github.com/box/box-python-sdk

Install
```sh
pip install bskillskit
```

Example
```python
from bskillskit import FileReader
from bskillskit import SkillsWriter
from bskillskit import SkillsErrorEnum

# Interpret the event from Box
json_req = { ... }

file_reader = FileReader(json_req)
skills_writer = SkillsWriter(json_req)

# Save a status update back to Box
skills_writer.saveProcessingCard()

# Download file from Box
with open(filereader.file_name, 'wb') as f:
    file_reader.download_to(f)

# Execute iference processing
result_is_not_error = True

if result_is_not_error:
    # Write metadata back to Box
    topi_card_json = skills_writer.create_topics_card(
        [
           { 'text': 'Hello' },
           { 'text': 'File' }
        ]
    )
    transcripts_card_json = skills_writer.create_transcripts_card(
        [
            {
                'text': 'Hello file',
                'appears': [
                    {
                        'start': 0,
                        'end': 1
                    }
                ]
            }
        ],
        1
    )
    face_card_json = skills_writer.create_faces_card(
        [
            {
                'text': "if image doesn't load this text is shown",
                'image_url': 'https://seeklogo.com/images/B/box-logo-646A3D8C91-seeklogo.com.png'
            }
        ],
        None,
        'Logos'
    )
    skills_writer.save_data_cards([topi_card_json, transcripts_card_json, face_card_json])
else:
    # Using error cards to display errors
    skills_writer.save_error_card(SkillsErrorEnum.INVALID_FILE_FORMAT)
```


