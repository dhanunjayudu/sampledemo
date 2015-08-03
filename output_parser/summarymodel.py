from cafe.engine.models.base import BaseModel

class SummaryModel(BaseModel):
    def __init__(
            self, account_nums=None, service_types=None, bill_nums=None, bill_start_date=None,
            bill_end_date=None, service_type=None, event_types=None,
            impact_types=None, quantity=None, uom=None, rate=None,
            amount=None, usage_record_id=None, dc_id=None,
            region_id=None, res_id=None, res_name=None,
            attribute_1=None, attribute_2=None, attribute_3=None):
        self.account_nums = account_nums or []
        self.service_types = service_types or []
        self.bill_nums = bill_nums or []
        self.bill_start_date = bill_start_date or []
        self.bill_end_date = bill_end_date or []
        self.event_types = event_types or []
        self.impact_types = impact_types or []
        self.quantity = quantity or []
        self.uom = uom or []
        self.rate = rate or []
        self.amount = amount or []
        self.usage_record_id = usage_record_id or []
        self.dc_id = dc_id or []
        self.region_id = region_id or []
        self.res_id = res_id or []
        self.res_name = res_name or []
        self.attribute_1 = attribute_1 or []
        self.attribute_2 = attribute_2 or []
        self.attribute_3 = attribute_3 or []