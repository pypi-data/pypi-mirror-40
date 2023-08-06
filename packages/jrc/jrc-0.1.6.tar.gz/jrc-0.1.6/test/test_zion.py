import os
from jrc import Compiler
from jrc import ZionExtension
from jrc.parser import parser_dict


def test_pipeline():
    dsl_str = """
    from ..lib.detailtable import *
    from ..lib.textbox import *
    mer_id = Textbox()
    mer_id.caption = "商户号"
    mer_id.id = "mer_id"
    mer_id.disabled = "true"
    
    user_config_info = DetailTable()
    user_config_info.id = "user_config_info"
    user_config_info.url = "http://192.168.15.239:8632/api/console/v1/query_user"
    # todo return_code
    user_config_info.return_code = "90000"
    user_config_info.data_node = "data"
    user_config_info.Column.field = "slbCustId|loanSwitch|loanLimit|userStatus"
    user_config_info.Column.title = "用户生利宝账号|T1赎回垫资开关|垫资额度|用户状态"
    """
    lang_tx_str = """
        TreeModel:
            imports+=Import
            nodes+=Node
        ;
        
        Import:
            'from' /[a-zA-Z0-9_.]*/ 'import *'
        ;
        
        Node:
            handler=ID'='name=ID'()'
            properties*=Property
            (ID'.'func=Func'()')?
        ;
        
        Property:
            Single | Nested
        ;
        
        Single:
            ID'.'key=ID '=' value=Value
        ;
        
        Nested:
            ID'.'ID'.'key=ID '=' value=Value
        ;
        
        Value:
            name=STRING
        ;
        
        Func:
            'show' | 'check'
        ;
        
        Comment:
            /#.*$/
        ;
    """

    out_code = """
    """
    my_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(my_path, '../demo/zion/template/')
    params = {
        'dsl_str': dsl_str,
        'lang_tx_str': parser_dict.get('python_tx'),
        'template_path': template_path,
        'extension':  ZionExtension(template_path=template_path)
    }
    my_parser = Compiler(**params)
    my_parser.compile()

