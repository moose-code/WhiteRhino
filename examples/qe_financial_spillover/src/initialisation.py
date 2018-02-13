from fund import Fund
from asset import Asset
from functions import *
from functions.distribute import *

import random

def init_funds(identifiers_funds, lambdas, thetas, phis, regions, asset_dict):
    #Instantiate investor funds using the number of identifiers as range
    fund_list = []
    # Loop over number of funds
    for ident, lambda_ , theta, phi  in zip(identifiers_funds, lambdas, thetas, phis):
        # Instantiate fund object
        fund = Fund(ident, lambda_, theta, phi)
         # Save in list
        fund_list.append(fund)

    fund_regions = distribute_funds_equally(len(identifiers_funds), regions)
    # Attach region to funds
    count_domestic = 0
    count_foreign = 0
    for fund, region_label in zip(fund_list, fund_regions):
        fund.parameters['region'] = region_label
        if "domestic" in fund.parameters['region']:
            count_domestic+=1
        if "foreign" in fund.parameters['region']:
            count_foreign += 1

    # Give balance sheets items to funds
    for asset, list in asset_dict.iteritems():
        for i in list:

            # exclude cash
            if "cash" not in i.identifier:
                asset_quantity =  distribute_funds_equally(len(identifiers_funds), [i.parameters['global_supply']/len(identifiers_funds)])

                for fund, quantity in zip(fund_list, asset_quantity):
                # We save a list with the object and quantity inside a dictionary attached to the fund
                    fund.assets[i.identifier] = [i, quantity]

            if "cash" in i.identifier:
            #check in which region we are
                for fund in fund_list:
                    # print fund.parameters['region'], fund.identifier, i.identifier
                    if "domestic" in fund.parameters['region'] and "domestic" in i.identifier:
                         fund.assets[i.identifier] = [i, i.parameters['global_supply']/count_domestic]
                    if "foreign" in fund.parameters['region'] and "foreign" in i.identifier:
                        fund.assets[i.identifier] = [i, i.parameters['global_supply'] / count_foreign]
    fund_size = 0
    # # Allocate fund size
    for fund in fund_list:
        for key, value in fund.assets.iteritems():
            fund_size += value[1]
        fund.liabilities = fund_size
    return fund_list

def get_fund_size(funds):
    global_capital = 0
    for fund in funds:
         global_capital+= fund.liabilities

    return global_capital

def init_assets(regions, identifiers_assets, ms, rhos, omegas, face_values, global_supply, prices):
    # Instantiate investor funds using the number of identifiers as range
    asset_dict = {}
      # Loop over regions
    for region in regions:
        temp = {
            region : {}
                }
        asset_dict.update(temp)

    domestic = []
    foreign = []

    for ident,  m, rho, omega, face_value, global_supply, price  in zip(identifiers_assets,  ms, rhos, omegas, face_values,global_supply, prices):
        # Instantiate fund object
        asset = Asset(ident, m, rho, omega, face_value, global_supply, price )

        # Save in dict - hard coded; not elegant and problematic if there are more regions
        if "domestic" in ident:
            domestic.append(asset)
        if "foreign" in ident:
            foreign.append(asset)

    for key, value in  asset_dict.iteritems():
        if "domestic" in key:
            asset_dict[key] = domestic
        if "foreign" in key:
            asset_dict[key] = foreign
    return  asset_dict

def init_returns(assets):
    for key, list in assets.iteritems():
        for asset in list:
            return_ = asset.parameters['rho']
            asset.returns.append(return_)