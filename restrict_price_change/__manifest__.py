# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Purchase Price Change Restriction",

    'summary': """
        Restrict price change on purchase orders""",

    'description': """
        
    """,

    'author': "",
    'website': "",
    'license': "",

    'category': 'Purchase',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        'security/price_change_security.xml',
        'views/purchase.xml',
    ],
    'images': [

    ],
    'installable': True,
}
