
# PYPI Packages
import usaddress, regex

STATE_DICTIONARY = {
    "ALABAMA":"AL",
    "ALASKA":"AK",
    "ARIZONA":"AZ",
    "ARKANSAS":"AR",
    "CALIFORNIA":"CA",
    "COLORADO":"CO",
    "CONNECTICUT":"CT",
    "DELAWARE":"DE",
    "DISTRICT OF COLUMBIA":"DC",
    "FLORIDA":"FL",
    "GEORGIA":"GA",
    "HAWAII":"HI",
    "IDAHO":"ID",
    "ILLINOIS":"IL",
    "INDIANA":"IN",
    "IOWA":"IA",
    "KANSAS":"KS",
    "KENTUCKY":"KY",
    "LOUISIANA":"LA",
    "MAINE":"ME",
    "MARYLAND":"MD",
    "MASSACHUSETTS":"MA",
    "MICHIGAN":"MI",
    "MINNESOTA":"MN",
    "MISSISSIPPI":"MS",
    "MISSOURI":"MO",
    "MONTANA":"MT",
    "NEBRASKA":"NE",
    "NEVADA":"NV",
    "NEW HAMPSHIRE":"NH",
    "NEW JERSEY":"NJ",
    "NEW MEXICO":"NM",
    "NEW YORK":"NY",
    "NORTH CAROLINA":"NC",
    "NORTH DAKOTA":"ND",
    "OHIO":"OH",
    "OKLAHOMA":"OK",
    "OREGON":"OR",
    "PENNSYLVANIA":"PA",
    "RHODE ISLAND":"RI",
    "SOUTH CAROLINA":"SC",
    "SOUTH DAKOTA":"SD",
    "TENNESSEE":"TN",
    "TEXAS":"TX",
    "UTAH":"UT",
    "VERMONT":"VT",
    "VIRGINIA":"VA",
    "WASHINGTON":"WA",
    "WEST VIRGINIA":"WV",
    "WISCONSIN":"WI",
    "WYOMING":"WY"
    }


STATE_ABBREVS = list(STATE_DICTIONARY.values())


def abbrev_state(string):
    if string.upper() in STATE_ABBREVS:
        return string.upper()
    elif string.upper() in STATE_DICTIONARY:
        return STATE_DICTIONARY[string.upper()]
    
    return None


def title(text):
    tokens = text.split(' ')
    capitalised = [i[0].upper() + i[1:] for i in tokens]
    final_text = ' '.join(capitalised)
    return final_text


def to_components(span, abbreviate_state=True, enforce_street=True):


    result_dict = {}


    # Remove new lines from address
    span = span.replace('\n', ' ')

    # Clean common words that may be inserted as part of address
    span = span.replace('address', '').strip()
    if 'city' in span and 'state' in span and 'zip' in span:
        span = span.replace('city','').replace('state','').replace('zip','').strip()

    # Removes space between hyphenated digits
    span = regex.sub('(\d)( - )(\d)',r'\1-\3', span)

    try:
        result = usaddress.tag(span)[0]
    except Exception as e:
        print("usaddress module failing {}".format(e))
        return result_dict  

    
    # Extract results from usadress module
    # sub_address_identifier = result.get('SubaddressIdentifier')
    address_number = result.get('AddressNumber')
    address_number_suffix = result.get('AddressNumberSuffix')
    street_name_predirectional = result.get('StreetNamePreDirectional')
    street_name_premodifier = result.get('StreetNamePreModifier')
    street_name_pretype = result.get('StreetNamePreType')
    street_name = result.get('StreetName')
    street_name_post = result.get('StreetNamePostType')
    street_name_postdirectional = result.get('StreetNamePostDirectional')
    city = result.get('PlaceName')


    # Split the city (PlaceName) out in to neighborhood and city results
    if city and ',' in city:
        split_city = city.split(',')
        neighborhood, city = split_city[-2], split_city[-1]
        city = city.strip()
        neighborhood = neighborhood.strip()
    else:
        neighborhood = None

    state_name = result.get('StateName')
    zip_code = result.get('ZipCode')

    include_street = True
    if (address_number == None or street_name == None):
        if enforce_street:
            return result_dict
        else:
            include_street = False

    # The splitting is mean to remove these errors
    # 000 6802 E 56th Street, Indianapolis, IN 46226
    address_string = address_number.split(' ')[-1]


    if address_number_suffix:
        address_string += ' ' + title(address_number_suffix)
    if street_name_predirectional and len(street_name_predirectional) <= 2:
        address_string += ' ' + street_name_predirectional.upper()
    elif street_name_predirectional:
        address_string += ' ' + street_name_predirectional
    if street_name_premodifier:
        address_string += ' ' + title(street_name_premodifier)
    if street_name_pretype:
        address_string += ' ' + title(street_name_pretype)
    address_string += ' ' + title(street_name)
    if street_name_post:
        address_string += ' ' + title(street_name_post)
    if street_name_postdirectional:
        address_string += ' ' + street_name_postdirectional.upper()

    result_dict['address'] = address_string

    if neighborhood:
        result_dict['neighborhood'] = neighborhood.title()

    if city:
        city = city.replace(' in ',' ')
        result_dict['city'] = city.title()

    if state_name:
        if abbreviate_state:
            result_dict['state'] = abbrev_state(state_name)
        else:
            result_dict['state'] = state_name

    if zip_code:
        result_dict['zip'] = zip_code

    return result_dict