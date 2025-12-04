"""
Thrift IDL Parser
Thrift IDL 解析器

解析 Thrift IDL 文件，提取结构体、服务定义等信息
"""
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ThriftField:
    """Thrift 字段"""
    id: int
    name: str
    type: str
    required: bool = True
    default: Optional[str] = None
    doc: Optional[str] = None


@dataclass
class ThriftStruct:
    """Thrift 结构体"""
    name: str
    fields: List[ThriftField] = field(default_factory=list)
    doc: Optional[str] = None


@dataclass
class ThriftException:
    """Thrift 异常"""
    name: str
    fields: List[ThriftField] = field(default_factory=list)
    doc: Optional[str] = None


@dataclass
class ThriftMethod:
    """Thrift 方法"""
    name: str
    return_type: str
    parameters: List[ThriftField] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    doc: Optional[str] = None


@dataclass
class ThriftService:
    """Thrift 服务"""
    name: str
    methods: List[ThriftMethod] = field(default_factory=list)
    doc: Optional[str] = None


@dataclass
class ThriftIDL:
    """Thrift IDL 定义"""
    namespace: Dict[str, str] = field(default_factory=dict)
    structs: List[ThriftStruct] = field(default_factory=list)
    exceptions: List[ThriftException] = field(default_factory=list)
    services: List[ThriftService] = field(default_factory=list)


class ThriftParser:
    """Thrift IDL 解析器"""
    
    # 类型映射：Thrift -> Python
    TYPE_MAPPING = {
        'i8': 'int',
        'i16': 'int',
        'i32': 'int',
        'i64': 'int',
        'double': 'float',
        'string': 'str',
        'bool': 'bool',
        'binary': 'bytes',
    }
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = ""
        
    def parse(self) -> ThriftIDL:
        """解析 Thrift 文件"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        idl = ThriftIDL()
        
        # 解析 namespace
        idl.namespace = self._parse_namespace()
        
        # 解析 struct
        idl.structs = self._parse_structs()
        
        # 解析 exception
        idl.exceptions = self._parse_exceptions()
        
        # 解析 service
        idl.services = self._parse_services()
        
        return idl
    
    def _parse_namespace(self) -> Dict[str, str]:
        """解析命名空间"""
        namespaces = {}
        pattern = r'namespace\s+(\w+)\s+([\w.]+)'
        matches = re.finditer(pattern, self.content)
        for match in matches:
            lang, ns = match.groups()
            namespaces[lang] = ns
        return namespaces
    
    def _parse_structs(self) -> List[ThriftStruct]:
        """解析结构体"""
        structs = []
        # 匹配 struct 定义
        pattern = r'struct\s+(\w+)\s*\{([^}]+)\}'
        matches = re.finditer(pattern, self.content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            struct_name = match.group(1)
            struct_body = match.group(2)
            
            # 提取文档注释
            doc = self._extract_doc_before(match.start())
            
            # 解析字段
            fields = self._parse_fields(struct_body)
            
            structs.append(ThriftStruct(
                name=struct_name,
                fields=fields,
                doc=doc
            ))
        
        return structs
    
    def _parse_exceptions(self) -> List[ThriftException]:
        """解析异常"""
        exceptions = []
        pattern = r'exception\s+(\w+)\s*\{([^}]+)\}'
        matches = re.finditer(pattern, self.content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            exc_name = match.group(1)
            exc_body = match.group(2)
            
            doc = self._extract_doc_before(match.start())
            fields = self._parse_fields(exc_body)
            
            exceptions.append(ThriftException(
                name=exc_name,
                fields=fields,
                doc=doc
            ))
        
        return exceptions
    
    def _parse_services(self) -> List[ThriftService]:
        """解析服务"""
        services = []
        pattern = r'service\s+(\w+)\s*\{([^}]+)\}'
        matches = re.finditer(pattern, self.content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            service_name = match.group(1)
            service_body = match.group(2)
            
            doc = self._extract_doc_before(match.start())
            methods = self._parse_methods(service_body)
            
            services.append(ThriftService(
                name=service_name,
                methods=methods,
                doc=doc
            ))
        
        return services
    
    def _parse_fields(self, body: str) -> List[ThriftField]:
        """解析字段列表"""
        fields = []
        # 匹配字段：1: required string name
        pattern = r'(\d+):\s*(required|optional)?\s*([^\s,]+)\s+(\w+)'
        matches = re.finditer(pattern, body)
        
        for match in matches:
            field_id = int(match.group(1))
            required_str = match.group(2)
            field_type = match.group(3)
            field_name = match.group(4)
            
            fields.append(ThriftField(
                id=field_id,
                name=field_name,
                type=self._convert_type(field_type),
                required=(required_str == 'required')
            ))
        
        return fields
    
    def _parse_methods(self, body: str) -> List[ThriftMethod]:
        """解析方法列表"""
        methods = []
        # 匹配方法定义
        pattern = r'(\w+)\s+(\w+)\s*\(([^)]*)\)(?:\s*throws\s*\(([^)]+)\))?'
        matches = re.finditer(pattern, body)
        
        for match in matches:
            return_type = match.group(1)
            method_name = match.group(2)
            params_str = match.group(3)
            throws_str = match.group(4)
            
            # 解析参数
            parameters = []
            if params_str.strip():
                param_pattern = r'(\d+):\s*([^\s,]+)\s+(\w+)'
                param_matches = re.finditer(param_pattern, params_str)
                for pm in param_matches:
                    parameters.append(ThriftField(
                        id=int(pm.group(1)),
                        name=pm.group(3),
                        type=self._convert_type(pm.group(2)),
                        required=True
                    ))
            
            # 解析异常
            exceptions = []
            if throws_str:
                exc_pattern = r'\d+:\s*(\w+)'
                exc_matches = re.finditer(exc_pattern, throws_str)
                exceptions = [m.group(1) for m in exc_matches]
            
            methods.append(ThriftMethod(
                name=method_name,
                return_type=self._convert_type(return_type),
                parameters=parameters,
                exceptions=exceptions
            ))
        
        return methods
    
    def _convert_type(self, thrift_type: str) -> str:
        """转换 Thrift 类型到 Python 类型"""
        # 处理容器类型
        if thrift_type.startswith('list<'):
            inner_type = thrift_type[5:-1]
            return f"List[{self._convert_type(inner_type)}]"
        elif thrift_type.startswith('map<'):
            types = thrift_type[4:-1].split(',')
            key_type = self._convert_type(types[0].strip())
            val_type = self._convert_type(types[1].strip())
            return f"Dict[{key_type}, {val_type}]"
        elif thrift_type.startswith('set<'):
            inner_type = thrift_type[4:-1]
            return f"Set[{self._convert_type(inner_type)}]"
        
        # 基础类型映射
        return self.TYPE_MAPPING.get(thrift_type, thrift_type)
    
    def _extract_doc_before(self, position: int) -> Optional[str]:
        """提取位置之前的文档注释"""
        # 查找最近的 /** ... */ 注释
        text_before = self.content[:position]
        pattern = r'/\*\*([^*]|\*(?!/))*\*/'
        matches = list(re.finditer(pattern, text_before, re.DOTALL))
        
        if matches:
            last_match = matches[-1]
            # 检查注释和当前位置之间只有空白
            between = text_before[last_match.end():position]
            if between.strip() == '':
                doc = last_match.group(0)
                # 清理注释格式
                doc = re.sub(r'/\*\*|\*/', '', doc)
                doc = re.sub(r'^\s*\*\s?', '', doc, flags=re.MULTILINE)
                return doc.strip()
        
        return None


def parse_thrift_file(filepath: str) -> ThriftIDL:
    """解析 Thrift 文件的便捷函数"""
    parser = ThriftParser(filepath)
    return parser.parse()
