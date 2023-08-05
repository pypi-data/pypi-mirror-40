import pytest

from pdblp import parser


def test_historical_data_request_empty():
    test_str = """
    HistoricalDataRequest = {
    }
    """
    res = parser.to_dict_list(test_str)
    exp_res = [{"HistoricalDataRequest": {}}]
    assert res == exp_res


def test_historical_data_request_two_empty():
    test_str = """
    HistoricalDataRequest = {
    }

    HistoricalDataRequest = {
    }
    """
    res = parser.to_dict_list(test_str)
    exp_res = [{"HistoricalDataRequest": {}},
               {"HistoricalDataRequest": {}}]
    assert res == exp_res


def test_historical_data_request_one_security_one_field_one_date():
    test_str = """
    HistoricalDataRequest = {
        securities[] = {
            "SPY US Equity"
        }
        fields[] = {
            "PX_LAST"
        }
        startDate = "20150630"
        endDate = "20150630"
        overrides[] = {
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataRequest":
               {"securities": ["SPY US Equity"],
                "fields": ["PX_LAST"],
                "startDate": "20150630",
                "endDate": "20150630",
                "overrides": []}
                }]
    assert res == exp_res


def test_historical_data_response_one_security_one_field_one_date():
    test_str = """
     HistoricalDataResponse = {
        securityData = {
            security = "SPY US Equity"
            eidData[] = {
            }
            sequenceNumber = 0
            fieldExceptions[] = {
            }
            fieldData[] = {
                fieldData = {
                    date = 2015-06-29
                    PX_LAST = 205.420000
                }
            }
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataResponse":
               {"securityData":
                {"security": "SPY US Equity",
                             "eidData": [],
                             "sequenceNumber": 0,
                             "fieldExceptions": [],
                             "fieldData": [{"fieldData": {"date": "2015-06-29", "PX_LAST": 205.42}}]  # NOQA
                 }
                }
               }]

    assert res == exp_res


def test_historical_data_response_one_security_one_field_multi_date():
    test_str = """
     HistoricalDataResponse = {
        securityData = {
            security = "SPY US Equity"
            eidData[] = {
            }
            sequenceNumber = 0
            fieldExceptions[] = {
            }
            fieldData[] = {
                fieldData = {
                    date = 2015-06-29
                    PX_LAST = 205.420000
                }
                fieldData = {
                    date = 2015-06-30
                    PX_LAST = 205.850000
                }
            }
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataResponse":
               {"securityData":
                {"security": "SPY US Equity",
                 "eidData": [],
                 "sequenceNumber": 0,
                 "fieldExceptions": [],
                 "fieldData": [{"fieldData": {"date": "2015-06-29", "PX_LAST": 205.42}},  # NOQA
                               {"fieldData": {"date": "2015-06-30", "PX_LAST": 205.85}}]  # NOQA
                 }
                }
               }]
    assert res == exp_res


def test_historical_data_request_two_securities_one_field():
    test_str = """
     HistoricalDataRequest = {
        securities[] = {
            "SPY US Equity", "TLT US Equity"
        }
        fields[] = {
            "PX_LAST"
        }
        startDate = "20150629"
        endDate = "20150630"
        overrides[] = {
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataRequest":
               {"securities": ["SPY US Equity", "TLT US Equity"],
                "fields": ["PX_LAST"],
                "startDate": "20150629",
                "endDate": "20150630",
                "overrides": []}
                }]
    assert res == exp_res


def test_historical_data_response_two_securities_one_field():
    test_str = """
    HistoricalDataResponse = {
        securityData = {
            security = "SPY US Equity"
            eidData[] = {
            }
            sequenceNumber = 0
            fieldExceptions[] = {
            }
            fieldData[] = {
                fieldData = {
                    date = 2015-06-29
                    PX_LAST = 205.420000
                }
                fieldData = {
                    date = 2015-06-30
                    PX_LAST = 205.850000
                }
            }
        }
    }

    HistoricalDataResponse = {
        securityData = {
            security = "TLT US Equity"
            eidData[] = {
            }
            sequenceNumber = 1
            fieldExceptions[] = {
            }
            fieldData[] = {
                fieldData = {
                    date = 2015-06-29
                    PX_LAST = 118.280000
                }
                fieldData = {
                    date = 2015-06-30
                    PX_LAST = 117.460000
                }
            }
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [
     {"HistoricalDataResponse":
       {"securityData":
        {"security": "SPY US Equity",
         "eidData": [],
         "sequenceNumber": 0,
         "fieldExceptions": [],
         "fieldData": [{"fieldData": {"date": "2015-06-29", "PX_LAST": 205.42}},  # NOQA
                       {"fieldData": {"date": "2015-06-30", "PX_LAST": 205.85}}]  # NOQA
         }
        }
       },
     {"HistoricalDataResponse":
       {"securityData":
        {"security": "TLT US Equity",
         "eidData": [],
         "sequenceNumber": 1,
         "fieldExceptions": [],
         "fieldData": [{"fieldData": {"date": "2015-06-29", "PX_LAST": 118.28}},  # NOQA
                       {"fieldData": {"date": "2015-06-30", "PX_LAST": 117.46}}]  # NOQA
         }
        }
       }
    ]
    assert res == exp_res


def test_historical_data_request_one_security_two_fields():
    test_str = """
     HistoricalDataRequest = {
        securities[] = {
            "SPY US Equity"
        }
        fields[] = {
            "PX_LAST", "VOLUME"
        }
        startDate = "20150629"
        endDate = "20150630"
        overrides[] = {
        }
     }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataRequest":
               {"securities": ["SPY US Equity"],
                "fields": ["PX_LAST", "VOLUME"],
                "startDate": "20150629",
                "endDate": "20150630",
                "overrides": []}
                }]
    assert res == exp_res


def test_historical_data_response_one_security_two_fields():
    test_str = """
     HistoricalDataResponse = {
        securityData = {
            security = "SPY US Equity"
            eidData[] = {
            }
            sequenceNumber = 0
            fieldExceptions[] = {
            }
            fieldData[] = {
                fieldData = {
                    date = 2015-06-29
                    PX_LAST = 205.420000
                    VOLUME = 202621332.000000
                }
                fieldData = {
                    date = 2015-06-30
                    PX_LAST = 205.850000
                    VOLUME = 182925106.000000
                }
            }
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataResponse":
               {"securityData":
                {"security": "SPY US Equity",
                             "eidData": [],
                             "sequenceNumber": 0,
                             "fieldExceptions": [],
                             "fieldData": [{"fieldData": {"date": "2015-06-29", "PX_LAST": 205.42, "VOLUME": 202621332}},  # NOQA
                                           {"fieldData": {"date": "2015-06-30", "PX_LAST": 205.85, "VOLUME": 182925106}}]  # NOQA
                 }
                }
               }]

    assert res == exp_res


def test_reference_data_request_override():
    test_str = """
     ReferenceDataRequest = {
        securities[] = {
            "AUD Curncy"
        }
        fields[] = {
            "SETTLE_DT"
        }
        overrides[] = {
            overrides = {
                fieldId = "REFERENCE_DATE"
                value = "20161010"
            }
        }
     }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"ReferenceDataRequest":
               {"securities": ["AUD Curncy"],
                "fields": ["SETTLE_DT"],
                "overrides": [{"overrides": {"fieldId": "REFERENCE_DATE", "value": "20161010"}}]  # NOQA
                 }
                }]
    assert res == exp_res


def test_reference_data_response_override():
    test_str = """
     ReferenceDataResponse = {
        securityData[] = {
            securityData = {
                security = "AUD Curncy"
                eidData[] = {
                }
                fieldExceptions[] = {
                }
                sequenceNumber = 0
                fieldData = {
                    SETTLE_DT = 2016-10-12
                }
            }
        }
     }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"ReferenceDataResponse":
               {"securityData":
                [{"securityData":
                  {"security": "AUD Curncy",
                   "eidData": [],
                   "fieldExceptions": [],
                   "sequenceNumber": 0,
                   "fieldData": {"SETTLE_DT": "2016-10-12"}
                   }
                  }
                 ]
                }
                }]
    assert res == exp_res


def test_reference_data_response_two_securities():
    test_str = """
     ReferenceDataResponse = {
        securityData[] = {
            securityData = {
                security = "AUD Curncy"
                eidData[] = {
                }
                fieldExceptions[] = {
                }
                sequenceNumber = 0
                fieldData = {
                    SETTLE_DT = 2017-05-23
                }
            }
            securityData = {
                security = "CAD Curncy"
                eidData[] = {
                }
                fieldExceptions[] = {
                }
                sequenceNumber = 1
                fieldData = {
                    SETTLE_DT = 2017-05-23
                }
            }
        }
     }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"ReferenceDataResponse":
               {"securityData":
                [{"securityData":
                  {"security": "AUD Curncy",
                   "eidData": [],
                   "fieldExceptions": [],
                   "sequenceNumber": 0,
                   "fieldData": {"SETTLE_DT": "2017-05-23"}
                   }
                  },
                 {"securityData":
                  {"security": "CAD Curncy",
                   "eidData": [],
                   "fieldExceptions": [],
                   "sequenceNumber": 1,
                   "fieldData": {"SETTLE_DT": "2017-05-23"}
                   }
                  }
                 ]
                }
                }]
    assert res == exp_res


def test_reference_data_response_futures_chain():
    test_str = """
    ReferenceDataResponse = {
        securityData[] = {
            securityData = {
                security = "CO1 Comdty"
                eidData[] = {
                }
                fieldExceptions[] = {
                }
                sequenceNumber = 0
                fieldData = {
                    FUT_CHAIN[] = {
                        FUT_CHAIN = {
                            Security Description = "CON7 Comdty"
                        }
                        FUT_CHAIN = {
                            Security Description = "COQ7 Comdty"
                        }
                    }
                }
            }
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"ReferenceDataResponse":
               {"securityData":
                [{"securityData":
                  {"security": "CO1 Comdty",
                   "eidData": [],
                   "fieldExceptions": [],
                   "sequenceNumber": 0,
                   "fieldData": {"FUT_CHAIN":
                                 [{"FUT_CHAIN": {"Security Description": "CON7 Comdty"}},  # NOQA
                                  {"FUT_CHAIN": {"Security Description": "COQ7 Comdty"}}]  # NOQA
                                 }
                   }
                  }
                 ]
                }
               }]
    assert res == exp_res


def test_reference_data_response_time():
    test_str = """
         ReferenceDataResponse = {
            securityData[] = {
                securityData = {
                    security = "AUD Curncy"
                    eidData[] = {
                    }
                    fieldExceptions[] = {
                    }
                    sequenceNumber = 0
                    fieldData = {
                        TIME = "18:33:47"
                        LAST_PRICE_TIME_TODAY = 18:33:47.000
                    }
                }
            }
        }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"ReferenceDataResponse":
               {"securityData":
                [{"securityData":
                  {"security": "AUD Curncy",
                   "eidData": [],
                   "fieldExceptions": [],
                   "sequenceNumber": 0,
                   "fieldData": {"TIME": "18:33:47",
                                 "LAST_PRICE_TIME_TODAY": "18:33:47.000"}
                   }
                  }
                 ]
                }
                }]
    assert res == exp_res


def test_historical_data_response_invalid_date():
    test_str = """
     HistoricalDataResponse = {
        responseError = {
            source = "bbdbh4"
            code = 31
            category = "BAD_ARGS"
            message = "Invalid end date specified [nid:247] "
            subcategory = "INVALID_END_DATE"
        }
     }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataResponse":
               {"responseError": {"source": "bbdbh4",
                                  "code": 31,
                                  "category": "BAD_ARGS",
                                  "message": "Invalid end date specified [nid:247] ",  # NOQA
                                  "subcategory": "INVALID_END_DATE"}
                 }
                }]
    assert res == exp_res


def test_historical_data_response_invalid_security():
    test_str = """
     HistoricalDataResponse = {
        securityData = {
            security = "UNKNOWN Equity"
            eidData[] = {
            }
            sequenceNumber = 0
            securityError = {
                source = "247::bbdbh2"
                code = 15
                category = "BAD_SEC"
                message = "Unknown/Invalid securityInvalid Security [nid:247] "
                subcategory = "INVALID_SECURITY"
            }
            fieldExceptions[] = {
            }
            fieldData[] = {
            }
        }
    }
    """  # NOQA
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataResponse":
               {"securityData":
                {"security": "UNKNOWN Equity",
                 "eidData": [],
                 "sequenceNumber": 0,
                 "securityError": {"source": "247::bbdbh2",
                                   "code": 15,
                                   "category": "BAD_SEC",
                                   "message": "Unknown/Invalid securityInvalid Security [nid:247] ",  # NOQA
                                   "subcategory": "INVALID_SECURITY"},
                 "fieldExceptions": [],
                 "fieldData": []
                 }
                }
               }]
    assert res == exp_res


def test_historical_data_response_invalid_field():
    test_str = """
     HistoricalDataResponse = {
        securityData = {
            security = "SPY US Equity"
            eidData[] = {
            }
            sequenceNumber = 0
            fieldExceptions[] = {
                fieldExceptions = {
                    fieldId = "UNKNOWN"
                    errorInfo = {
                        source = "247::bbdbh3"
                        code = 1
                        category = "BAD_FLD"
                        message = "Invalid field"
                        subcategory = "NOT_APPLICABLE_TO_HIST_DATA"
                    }
                }
            }
            fieldData[] = {
                fieldData = {
                    date = 2015-06-29
                    PX_LAST = 205.420000
                }
                fieldData = {
                    date = 2015-06-30
                    PX_LAST = 205.850000
                }
            }
        }
    }
    """  # NOQA
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataResponse":
               {"securityData":
                {"security": "SPY US Equity",
                 "eidData": [],
                 "sequenceNumber": 0,
                 "fieldExceptions": [{"fieldExceptions":
                                      {"fieldId": "UNKNOWN",
                                       "errorInfo": {"source": "247::bbdbh3",  # NOQA
                                                     "code": 1,
                                                     "category": "BAD_FLD",
                                                     "message": "Invalid field",  # NOQA
                                                     "subcategory": "NOT_APPLICABLE_TO_HIST_DATA"}  # NOQA
                                       }
                                      }],
                 "fieldData": [{"fieldData": {"date": "2015-06-29", "PX_LAST": 205.42}},  # NOQA
                               {"fieldData": {"date": "2015-06-30", "PX_LAST": 205.85}}]  # NOQA

                 }
                }
               }]
    assert res == exp_res


def test_historical_data_response_nan():
    test_str = """
     HistoricalDataResponse = {
        securityData = {
            security = "EDM98 Comdty"
            eidData[] = {
            }
            sequenceNumber = 66
            fieldExceptions[] = {
            }
            fieldData[] = {
                fieldData = {
                    date = 1996-07-08
                    PX_SETTLE = 92.910000
                    PX_HIGH = nan
                    PX_LOW = nan
                    PX_OPEN = 92.870000
                }
            }
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"HistoricalDataResponse":
                {"securityData":
                 {"security": "EDM98 Comdty",
                  "eidData": [],
                  "sequenceNumber": 66,
                  "fieldExceptions": [],
                  "fieldData":
                  [
                   {"fieldData": {"date": "1996-07-08",
                                  "PX_SETTLE": 92.91,
                                  "PX_HIGH": "nan",
                                  "PX_LOW": "nan",
                                  "PX_OPEN": 92.87}
                    }
                  ]
                  }
                 }
                }]
    assert res == exp_res


@pytest.mark.xfail
def test_intradaybar_data_response():
    test_str = """
    IntradayBarResponse = {
        barData = {
            eidData[] = {
            }
            barTickData[] = {
                barTickData = {
                    time = 2018-12-11T10:55:00.000
                    open = 1.339800
                    high = 1.339900
                    low = 1.339700
                    close = 1.339900
                    volume = 0
                    numEvents = 1704
                    value = 0.000000
                }
                barTickData = {
                    time = 2018-12-11T11:00:00.000
                    open = 1.339900
                    high = 1.340000
                    low = 1.339700
                    close = 1.339800
                    volume = 0
                    numEvents = 2100
                    value = 0.000000
                }
            }
        }
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"IntradayBarResponse":
                {"barData":
                 {"eidData": [],
                  "barTickData":
                  [
                   {"barTickData": {"time": "2018-12-11T10:55:00.000",
                                    "open": 1.3398,
                                    "high": 1.3399,
                                    "low": 1.3397,
                                    "close": 1.3399,
                                    "volume": 0,
                                    "numEvents": 1704,
                                    "value": 0}
                    },
                   {"barTickData": {"time": "2018-12-11T11:00:00.000",
                                    "open": 1.3399,
                                    "high": 1.34,
                                    "low": 1.3397,
                                    "close": 1.3398,
                                    "volume": 0,
                                    "numEvents": 2100,
                                    "value": 0}
                    }
                  ]
                  }
                 }
                }]
    assert res == exp_res


@pytest.mark.xfail
def test_grid_response():
    test_str = """
    GridResponse = {
        NumOfFields = 0
        NumOfRecords = 2000
        ColumnTitles[] = {
            "TICKER", "VESSEL NAME"
        }
        DataRecords[] = {
            DataRecords = {
                DataFields[] = {
                    DataFields = {
                        StringValue = "IMO1000019 Index"
                    }
                    DataFields = {
                        StringValue = "LADY K II"
                    }
                }
            }
            DataRecords = {
                DataFields[] = {
                    DataFields = {
                        StringValue = "IMO6919837 Index"
                    }
                    DataFields = {
                        StringValue = "CAERUS"
                    }
                }
            }
        }
        ReachMax = false
        SequenceNumber = 0
    }
    """
    res = parser.to_dict_list(test_str)

    exp_res = [{"GridResponse":
                {"NumOfFields": 0,
                 "NumOfRecords": 2000,
                 "ColumnsTitles": ["TICKER", "VESSEL NAME"],
                 "DataRecords":
                  [
                   {"DataRecords": {'DataFields': [{'DatFields': {"StringValue": "IMO1000019 Index"}},  # NOQA
                                                   {'DatFields': {"StringValue": "LADY K II"}}]}},  # NOQA
                   {"DataRecords": {'DataFields': [{'DatFields': {"StringValue": "IMO6919837 Index"}},  # NOQA
                                                   {'DatFields': {"StringValue": "CAERUS"}}]}}  # NOQA
                  ],
                  "ReachMax": False,
                  "SequenceNumber": 0
                 }
                }]
    assert res == exp_res
