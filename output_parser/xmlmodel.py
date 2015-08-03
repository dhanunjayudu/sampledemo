from ubcafe.brm.output_parser.base import BaseXmlModel

class ParseBillingXml(BaseXmlModel):
    def __init__(self, id_=None, accounts=None):
        super(ParseBillingXml, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return cls(
            id_=data.attrib.get("id"),
            accounts=cls._build_list_model(cls._find(data, "accounts"),
                                           "account", AccountModel))

class AccountModel(BaseXmlModel):
    def __init__(self, rated_usages=None, account_id=None,
                 currency=None, contract_entity=None):
        super(AccountModel, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, data):
        #print data.attrib, data.text, data._children
        return cls(
            rated_usages=cls._build_list_model(cls._find(data, "rated_usages"),
                                               "rated_usage", RatedUsageModel),
            account_id=data.attrib.get("account_id"),
            currency=data.attrib.get("currency"),
            contract_entity=data.attrib.get("contract_entity"))

class RatedUsageModel(BaseXmlModel):
    def __init__(self, attributes=None, record_id=None, resource_id=None, resource_name=None,
                 service_name=None, event_type=None, charge_name=None,
                 rate_plan=None, amount=None, usage_metric=None, quantity=None,
                 rate=None, unit_of_measure=None, geo=None, region=None,
                 data_center=None, tax_flag=None):
        super(RatedUsageModel, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, data):

        return cls(
            attributes=cls._build_dict_from_xml(cls._find(data, "attributes")),
            record_id=data.attrib.get("record_id"),
            resource_id=data.attrib.get("resource_id"),
            resource_name=data.attrib.get("resource_name"),
            service_name=data.attrib.get("service_name"),
            event_type=data.attrib.get("event_type"),
            charge_name=data.attrib.get("charge_name"),
            rate_plan=data.attrib.get("rate_plan"),
            amount=data.attrib.get("amount"),
            usage_metric=data.attrib.get("usage_metric"),
            quantity=data.attrib.get("quantity"),
            rate=data.attrib.get("rate"),
            unit_of_measure=data.attrib.get("unit_of_measure"),
            geo=data.attrib.get("geo"),
            region=data.attrib.get("region"),
            data_center=data.attrib.get("data_center"),
            tax_flag=data.attrib.get("tax_flag"))

    @classmethod
    def _build_dict_from_xml(cls, data):
        dic = {}
        for child in data:
            dic[child.attrib.get("name")] = child.attrib.get("value")
        return dic