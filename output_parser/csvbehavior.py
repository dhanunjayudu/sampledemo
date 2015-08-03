from cafe.engine.behaviors import BaseBehavior
from ubcafe.brm.output_parser.summarymodel import SummaryModel
from itertools import groupby
from operator import itemgetter
import csv

class CSVBehavior(BaseBehavior):
    def __init__(self, csv_file):
        super(CSVBehavior, self).__init__()
        self.csv_file = csv_file

    def csv_summary(self, product=None, searchtype=None):
        summary_model = SummaryModel()
        values_list, account_nums, service_types, event_types, \
        impact_types, quantity, uom, rate, amount, usage_rec_ids, dc_ids, \
        region_ids, res_ids, res_names, attribute_1, attribute_2, \
        attribute_3 = ([] for i in range(17))
        searchtype_col = ""
        for row in csv.DictReader(open(self.csv_file)):
            values_list.append(row)
            if searchtype is not None:
                for header, detail in row.iteritems():
                    if detail.lower() == searchtype.lower():
                        searchtype_col = header
        if searchtype_col is not "":
            grouper = itemgetter("SERVICE_TYPE", searchtype_col)
        else:
            grouper = itemgetter("SERVICE_TYPE")
        for key, grp in groupby(sorted(values_list, key=grouper), grouper):
            for item in grp:
                if product is None:
                    service_types.append(item["SERVICE_TYPE"])
                elif product is not None and searchtype is not None:
                    if (item["SERVICE_TYPE"].lower() == product.lower()
                            and item[searchtype_col].lower() == searchtype.lower()):
                        amount.append(item["AMOUNT"])
                elif product is not None and searchtype is None:
                    if item["SERVICE_TYPE"].lower() == product.lower():
                        account_nums.append(item["ACCOUNT_NO"])
                        service_types.append(item["SERVICE_TYPE"])
                        event_types.append(item["EVENT_TYPE"])
                        impact_types.append(item["IMPACT_TYPE"])
                        quantity.append(item["QUANTITY"])
                        uom.append(item["UOM"])
                        rate.append(item["RATE"])
                        amount.append(item["AMOUNT"])
                        usage_rec_ids.append(item["USAGE_RECORD_ID"])
                        dc_ids.append(item["DC_ID"])
                        region_ids.append(item["REGION_ID"])
                        res_ids.append(item["RES_ID"])
                        res_names.append(item["RES_NAME"])
                        attribute_1.append(item["ATTRIBUTE_1"])
                        attribute_2.append(item["ATTRIBUTE_2"])
                        attribute_3.append(item["ATTRIBUTE_3"])
        summary_model.account_nums = set(account_nums)
        summary_model.service_types = set(service_types)
        summary_model.event_types = set(event_types)
        summary_model.impact_types = set(impact_types)
        summary_model.quantity = set(quantity)
        summary_model.uom = set(uom)
        summary_model.rate = set(rate)
        summary_model.amount = sum([float(x) for x in amount])
        summary_model.usage_record_id = set(usage_rec_ids)
        summary_model.dc_id = set(dc_ids)
        summary_model.region_id = set(region_ids)
        summary_model.res_id = set(res_ids)
        summary_model.res_name = set(res_names)
        summary_model.attribute_1 = set(attribute_1)
        summary_model.attribute_2 = set(attribute_2)
        summary_model.attribute_3 = set(attribute_3)

        return summary_model