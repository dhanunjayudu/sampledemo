from cafe.engine.behaviors import BaseBehavior
from ubcafe.brm.output_parser.xmlmodel import ParseBillingXml
from ubcafe.brm.output_parser.summarymodel import SummaryModel

class XMLBehavior(BaseBehavior):
    def __init__(self, xml_file):
        super(XMLBehavior, self).__init__()
        self.xml_file = xml_file

    def xml_summary(self, product=None, searchtype=None):
        summary_model = SummaryModel()
        values_list, account_nums, service_types, event_types, \
        impact_types, quantity, uom, rate, amount, usage_rec_ids, dc_ids, \
        region_ids, res_ids, res_names, attribute_1 = ([] for i in range(15))
        myfile = open (self.xml_file,"r")
        data=myfile.read().replace('\n','')
        m = ParseBillingXml._xml_to_obj(data)
        for usage in m.accounts[0].rated_usages:
            if product is None:
                service_types.append(usage.service_name)
            elif product is not None and searchtype is None:
                if usage.service_name.lower() == product.lower():
                    service_types.append(usage.service_name)
                    event_types.append(usage.event_type)
                    quantity.append(usage.quantity)
                    uom.append(usage.unit_of_measure)
                    rate.append(usage.rate)
                    amount.append(usage.amount)
                    usage_rec_ids.append(usage.record_id)
                    dc_ids.append(usage.data_center)
                    region_ids.append(usage.region)
                    res_ids.append(usage.resource_id)
                    res_names.append(usage.resource_name)
                    attribute_1.append(usage.attributes)
        summary_model.service_types = set(service_types)
        summary_model.event_types = set(event_types)
        summary_model.quantity = set(quantity)
        summary_model.uom = set(uom)
        summary_model.rate = set(rate)
        summary_model.amount = sum([float(x) for x in amount])
        summary_model.usage_record_id = set(usage_rec_ids)
        summary_model.dc_id = set(dc_ids)
        summary_model.region_id = set(region_ids)
        summary_model.res_id = set(res_ids)
        summary_model.res_name = set(res_names)
        summary_model.attribute_1 = attribute_1

        return summary_model