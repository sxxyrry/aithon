import re
import os
from typing import TypedDict, Literal


# Allowed Norms Names
AllowedNormsNames = [
    "AITC",
    "AITEP",
    "AITCN",
    "AITSC",
    "AITD",
]
class AITNParseMetadata(TypedDict):
    name: str
    author: str
    version: str
    affiliation : Literal[
        "AITC",
        "AITEP",
        "AITCN",
        "AITSC",
        "AITD",
    ]
class AITNParseRes(TypedDict):
    metadata: AITNParseMetadata
    content: str
    

class AITNParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def parse(self) -> AITNParseRes:
        metadata: AITNParseMetadata = {
            'name': '',
            'author': '',
            'version': '',
            'affiliation': ''
        }
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = f.read()
            
        # Parse metadata (key%value pairs)
        meta_pattern = r'^([^%]+)%(.+)$'
        for line in data.split('\n'):
            if line.startswith('<content>'):
                break
            match = re.match(meta_pattern, line)
            if match:
                key, value = match.groups()
                if key.strip() in ['author', 'name', 'version', 'affiliation']:
                    if key.strip() == 'affiliation':
                        if os.path.split(self.file_path)[1] == 'AITN0.aitn':
                            metadata['affiliation'] = 'AITN0.aitn'
                        elif value.strip() not in AllowedNormsNames:
                            raise Exception(f'无效的标准 {value.strip()}')

                    metadata[key.strip()] = value.strip()
                else:
                    raise Exception(f'无效的元数据 {key.strip()}')
                
        # Parse content
        content_match = re.search(r'<content>(.*?)</content>', data, re.DOTALL)
        if content_match:
            content = content_match.group(1).strip()
        else:
            content = ''
            
        if 'name' not in metadata:
            raise Exception('AITN 文件必须包含 name         字段')
        if 'author' not in metadata:
            raise Exception('AITN 文件必须包含 author       字段')
        if 'version' not in metadata:
            raise Exception('AITN 文件必须包含 version      字段')
        if 'affiliation' not in metadata:
            raise Exception('AITN 文件必须包含 affiliation  字段')
        if not content:
            raise Exception('AITN 文件必须包含 content      字段')

        return {
            'metadata': metadata,
            'content': content
        }

# Example usage:
if __name__ == '__main__':
    parser = AITNParser('d:/procedure/aithon/AITN/AITN0.aitn')
    result = parser.parse()
    print("Metadata:", result['metadata'])
    print("Content:", result['content'])
    print()