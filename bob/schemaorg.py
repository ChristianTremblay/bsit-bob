"""
Schema Org for the Bob Ontology
"""

import re
from typing import Union, get_args, get_origin, get_type_hints

from rdflib import Literal, URIRef
from rdflib.namespace import XSD

from bob.core import QUDT, SCHEMAORG
from bob.core import Node as _Node

_namespace = SCHEMAORG

"""
Schema.org is a collaborative, community-driven project that provides a collection of schemas for structured data on the internet. It is used to mark up web pages with metadata that can be understood by search engines and other applications, enabling better indexing and understanding of the content.

This implementation defines a minimal set of classes and properties based on the Schema.org vocabulary, focusing on the core concepts and types that are commonly used in the creation of models following 223P.

Class definitions have been simplified by using Literal instead of schema.org classes as
rdflib does not support the full range of schema.org types. Instead, we use Literal with appropriate datatypes to represent common values such as dates, times, URIs, and booleans.
This opens the door to possible violation of the schema that will be seen in the validation process

"""


def guess_literal_type(value: str) -> Literal:
    # Regex patterns
    uri_pattern = re.compile(r"^https?://[^\s]+$")
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    datetime_pattern = re.compile(
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|([+-]\d{2}:\d{2}))?$"
    )
    time_pattern = re.compile(r"^\d{2}:\d{2}(:\d{2})?$")
    int_pattern = re.compile(r"^-?\d+$")
    float_pattern = re.compile(r"^-?\d+\.\d+$")
    bool_pattern = re.compile(r"^(true|false)$", re.IGNORECASE)

    # URI
    if uri_pattern.match(value):
        return URIRef(value)
    # DateTime
    elif datetime_pattern.match(value):
        return Literal(value, datatype=XSD.dateTime)
    # Date
    elif date_pattern.match(value):
        return Literal(value, datatype=XSD.date)
    # Time
    elif time_pattern.match(value):
        return Literal(value, datatype=XSD.time)
    # Boolean
    elif bool_pattern.match(value):
        return Literal(value.lower() == "true", datatype=XSD.boolean)
    # Integer
    elif int_pattern.match(value):
        return Literal(int(value), datatype=XSD.integer)
    # Float
    elif float_pattern.match(value):
        return Literal(float(value), datatype=XSD.decimal)
    # Default: treat as string
    else:
        return Literal(value)


# == Nodes
class Thing(_Node):
    """
    The most generic type of item.
    """

    additionalType: Union[Literal, URIRef]
    alternateName: Literal
    description: Literal
    disambiguatingDescription: Literal
    identifier: Union[Literal, URIRef, "PropertyValue"]
    image: Union[URIRef, "ImageObject"]
    mainEntityOfPage: Union[URIRef, "CreativeWork"]
    name: Literal
    potentialAction: "Action"
    sameAs: Union[URIRef, "CreativeWork"]
    subjectOf: Union["CreativeWork", "Event"]
    url: URIRef

    def __init__(self, *args, **kwargs):
        hints = get_type_hints(self.__class__)
        for key, expected_type in hints.items():
            if key.startswith("_"):
                # Skip private attributes
                continue

            if key in kwargs:
                if get_origin(expected_type) is Union:
                    union_types = get_args(expected_type)
                    if Literal in union_types:
                        # If Literal is part of the union, we can use it directly
                        # by default, when no explicit type is provided, we assume Literal
                        expected_type = Literal
                    elif URIRef in union_types:
                        # If URIRef is part of the union, we can use it directly
                        expected_type = URIRef
                    else:
                        # If the expected type is not a Union, we can use it directly
                        raise ValueError(
                            f"You must provide an explicit type for {key} in {self.__class__.__name__}. Expected one of: {union_types}"
                        )
                value = kwargs[key]
                # Intercept and convert str to URIRef if needed
                if expected_type is URIRef and isinstance(value, str):
                    kwargs[key] = URIRef(value)
                elif expected_type is Literal:
                    kwargs[key] = guess_literal_type(value)

        super().__init__(*args, **kwargs)


class ImageObject(Thing):
    """
    An ImageObject is a representation of an image, which can include additional information such as the image URIRef, caption, and copyright.
    """

    contentUrl: URIRef  # URIRef of the image
    caption: Literal  # Caption or description of the image


class CreativeWork(Thing):
    """
    A CreativeWork is a work of art, literature, or other creative expression.
    It can include additional information such as the author, publication date, and license.
    """

    pass


class Certification(CreativeWork):
    """
    A Certification is an official and authoritative statement about a subject, for example a product, service, person, or organization. A certification is typically issued by an indendent certification body, for example a professional organization or government. It formally attests certain characteristics about the subject, for example Organizations can be ISO certified, Food products can be certified Organic or Vegan, a Person can be a certified professional, a Place can be certified for food processing. There are certifications for many domains: regulatory, organizational, recycling, food, efficiency, educational, ecological, etc. A certification is a form of credential, as are accreditations and licenses. Mapped from the gs1:CertificationDetails class in the GS1 Web Vocabulary.
    """

    about: Thing  # The subject of the certification, e.g. a product, service, person, or organization
    auditDate: Literal  # The date when the certification was audited
    certificationIdentification: Union[
        Literal, "DefinedTerm"
    ]  # The identification number or code of the certification
    # certificationRating: Rating
    certificationStatus: "CertificationStatusEnumeration"
    datePublished: Literal  # The date when the certification was published
    expires: Literal  # The date when the certification expires
    hasMeasurement: (
        "QuantitativeValue"  # The measurement details related to the certification
    )
    issuedBy: "Organization"  # The organization that issued the certification
    logo: Union[URIRef, ImageObject]  # The logo associated with the certification
    validFrom: Literal  # The date from which the certification is valid
    validIn: (
        "AdministrativeArea"  # The administrative area where the certification is valid
    )


class DefinedTermSet(CreativeWork):
    """
    A DefinedTermSet is a collection of terms that have specific meanings within a particular context.
    It can include additional information such as the terms' definitions, scope, and usage.
    """

    hasDefinedTerm: "DefinedTerm"


class Action(Thing):
    """
    An Action is a specific action that can be performed, such as a user interaction or a system operation.
    It can include additional information such as the target of the action and the result of the action.
    """

    pass


class Event(Thing):
    """
    An Event is an occurrence or happening, such as a concert, conference, or meeting.
    It can include additional information such as the date, time, location, and participants.
    """

    pass


class Intangible(Thing):
    """
    Intangible items are those that do not have a physical presence, such as concepts, ideas, or services.
    """

    pass


class StructuredValue(Intangible):
    """
    A StructuredValue is a value that has a specific structure, such as a property value or a measurement.
    It can include additional information such as the unit of measurement or the value type.
    """

    pass


class Quantity(Intangible):
    """
    Quantities such as distance, time, mass, weight, etc. Particular instances of say Mass are entities like '3 kg' or '4 milligrams'.
    """

    pass


class Mass(Quantity):
    """
    Properties that take Mass as values are of the form '<Number> <Mass unit of measure>'. E.g., '7 kg'.
    """

    pass


class EnergyConsumptionDetails(Intangible):
    """
    EnergyConsumptionDetails represents information related to the energy efficiency of a product that consumes energy. The information that can be provided is based on international regulations such as for example EU directive 2017/1369 for energy labeling and the Energy labeling rule under the Energy Policy and Conservation Act (EPCA) in the US.
    """

    energyEfficiencyScaleMax: "EUEnergyEfficiencyEnumeration"
    energyEfficiencyScaleMin: "EUEnergyEfficiencyEnumeration"
    hasEnergyEfficiencyCategory: "EUEnergyEfficiencyEnumeration"


class Distance(Quantity):
    """
    Properties that take Distances as values are of the form '<Number> <Length unit of measure>'. E.g., '7 ft'.
    """

    pass


class Language(Intangible):
    """
    Natural languages such as Spanish, Tamil, Hindi, English, etc. Formal language code tags expressed in BCP 47 can be used via the alternateName property. The Language type previously also covered programming languages such as Scheme and Lisp, which are now best represented using ComputerLanguage.
    """

    pass


class EducationalOccupationalProgram(Intangible):
    """
    A program offered by an institution which determines the learning progress to achieve an outcome, usually a credential like a degree or certificate. This would define a discrete set of opportunities (e.g., job, courses) that together constitute a program with a clear start, end, set of requirements, and transition to a new occupational opportunity (e.g., a job), or sometimes a higher educational opportunity (e.g., an advanced degree).
    """

    pass


class Duration(Quantity):
    """
    Quantity: Duration (use ISO 8601 duration format).
    """

    pass


class ContactPoint(StructuredValue):
    """
    A contact point—for example, a Customer Complaints department.
    """

    areaServed: Union[
        Literal, "Place", "AdministrativeArea", "GeoShape"
    ]  # The area served by the contact point
    availableLanguage: Union[
        Literal, "Language"
    ]  # The language(s) available for the contact point
    contactOption: "ContactPointOption"  # The contact options available, e.g. 'TollFree', 'HearingImpairedSupported'
    contactType: (
        Literal  # The type of contact, e.g. 'customer service', 'technical support'
    )
    email: Literal  # The email address for the contact point
    faxNumber: Literal  # The fax number for the contact point
    hoursAvailable: "OpeningHoursSpecification"  # The hours during which the contact point is available
    productSupported: Union[
        Literal, "Product"
    ]  # The product or service supported by the contact point
    telephone: Literal  # The telephone number for the contact point


class GeoShape(StructuredValue):
    """
    The geographic shape of a place. A GeoShape can be described using several properties whose values are based on latitude/longitude pairs. Either whitespace or commas can be used to separate latitude and longitude; whitespace should be used when writing a list of several such points.
    """

    address: Union["PostalAddress", Literal]  # The address of the geographic shape
    addressCountry: Union[Literal, "Country"]  # The country of the geographic shape
    box: Literal  # The bounding box of the geographic shape, represented as a string of latitude and longitude pairs
    circle: Literal  # The circle representing the geographic shape, represented as a string of latitude and longitude pairs
    elevation: Literal  # The elevation of the geographic shape, in meters
    line: Literal  # The line representing the geographic shape, represented as a string of latitude and longitude pairs
    polygon: Literal  # The polygon representing the geographic shape, represented as a string of latitude and longitude pairs
    postalCode: Literal  # The postal code of the geographic shape


class OpeningHoursSpecification(StructuredValue):
    """
        A structured value providing information about the opening hours of a place or a certain service inside a place.

    The place is open if the opens property is specified, and closed otherwise.

    If the value for the closes property is less than the value for the opens property then the hour range is assumed to span over the next day.
    """

    dayOfWeek: "DayOfWeek"  # The day of the week for the opening hours
    opens: Literal  # The time when the place or service opens
    closes: Literal  # The time when the place or service closes
    validFrom: Literal  # The date and time from which the opening hours are valid
    validThrough: Literal  # The date and time until which the opening hours are valid


class GeoCoordinates(StructuredValue):
    """
    The geographic coordinates of a place, represented as latitude and longitude.
    """

    latitude: Literal  # The latitude of the place
    longitude: Literal  # The longitude of the place
    elevation: Literal  # The elevation of the place, in meters
    postalCode: Literal  # The postal code of the place
    addressCountry: Union[Literal, "Country"]  # The country of the place
    address: Union["PostalAddress", Literal]  # The address of the place


class ServicePeriod(StructuredValue):
    """
    ServicePeriod represents a duration with some constraints about cutoff time and business days. This is used e.g. in shipping for handling times or transit time.
    """

    businessDays: Union[
        "DayOfWeek", "OpeningHoursSpecification"
    ]  # The business days during which the service is available
    cutoffTime: Literal  # The cutoff time for the service period
    duration: Union[
        "Duration", "QuantitativeValue"
    ]  # The duration of the service period


class DefinedTerm(Intangible):
    """
    A DefinedTerm is a term that has a specific meaning within a particular context.
    It can include additional information such as the term's definition, scope, and usage.
    """

    termCode: Literal
    inDefinedTermSet: Union[
        "DefinedTermSet", URIRef
    ]  # The set to which this term belongs


class Service(Intangible):
    """
    A service provided by an organization, e.g. delivery service, print services, etc.
    """

    # aggregateRating: "AggregateRating"  # An aggregate rating of the service
    areaServed: Union[
        Literal, "Place", "AdministrativeArea", "GeoShape"
    ]  # The area served by the service
    # audience: "Audience"  # The audience for the service
    availableChannel: Union[
        "ServiceChannel", "ContactPoint"
    ]  # The channel through which the service is available
    award: Literal  # An award won by the service
    broker: Union["Organization", "Person"]  # The broker of the service, if applicable
    category: Union[
        Literal,
        "CategoryCode",
        "DefinedTerm",
        Thing,
        URIRef,
        "PhysicalActivityCategory",
    ]  # The category of the service, e.g. 'delivery', 'print', 'consulting'
    hasCertification: Certification  # Certification details for the service
    # hasOfferCatalog: "OfferCatalog"  # The catalog of offers provided by the service
    hoursAvailable: (
        "OpeningHoursSpecification"  # The hours during which the service is available
    )
    isRelatedTo: Union["Service", "Product"]  # Related services or products
    isSimilarTo: Union["Service", "Product"]  # Similar services or products
    logo: Union[URIRef, "ImageObject"]  # The logo associated with the service
    # offers: Union["Offer", "Demand"]  # The offers available for the service
    provider: Union["Organization", "Person"]  # The provider of the service
    providerMobility: (
        Literal  # The mobility of the service provider, e.g. 'stationary', 'mobile'
    )
    # review: "Review"  # Reviews or aggregate ratings of the service
    serviceOutput: Thing  # The output of the service, e.g. a product or another service
    serviceType: Union["GovernmentBenefitsType", Literal]
    slogan: Literal  # A slogan associated with the service
    termsOfService: Union[URIRef, Literal]  # The terms of service for the service


class ServiceChannel(Intangible):
    """
    A channel through which a service is provided, such as a website, phone number, or physical location.
    It can include additional information such as the channel's type and availability.
    """

    availableLanguage: Union[
        Literal, "Language"
    ]  # The language(s) available for the service channel
    processingTime: Duration  # The processing time for the service channel
    providesService: Service  # The service provided through the channel
    serviceLocation: "Place"  # The location where the service is provided, e.g. a physical address or a virtual location
    servicePhone: ContactPoint  # The phone number for the service channel
    servicePostalAddress: "PostalAddress"  # The postal address for the service channel
    serviceSmsNumber: ContactPoint  # The SMS number for the service channel
    serviceUrl: URIRef  # The URIRef of the service channel


class CategoryCode(DefinedTerm):
    """
    A Category Code.
    """

    codeValue: Literal  # The value of the category code
    inCodeSet: Union[
        "CategoryCodeSet", URIRef
    ]  # The set to which this category code belongs


class CategoryCodeSet(DefinedTermSet):
    """
    A set of Category Code values.
    """

    hasCategoryCode: CategoryCode


class Enumeration(Intangible):
    """
    An Enumeration is a specific type of DefinedTerm that represents a set of values or options.
    It can include additional information such as the term's definition and scope.
    """

    supersededBy: Union["SchemaOrgClass", "SchemaOrgProperty", "Enumeration"]


class ContactPointOption(Enumeration):
    """
    Enumerated options related to a ContactPoint.
    """

    pass


class CertificationStatusEnumeration(Enumeration):
    """
    Enumerates the different statuses of a Certification (Active and Inactive).
    """

    pass


class OfferItemCondition(Enumeration):
    """
    A list of possible conditions for the item.
    """

    pass


class PhysicalActivityCategory(Enumeration):
    """
    Categories of physical activity, organized by physiologic classification.
    """

    pass


class GovernmentBenefitsType(Enumeration):
    """
    GovernmentBenefitsType enumerates several kinds of government benefits to support the COVID-19 situation. Note that this structure may not capture all benefits offered.

    """

    pass


class EnergyEfficiencyEnumeration(Enumeration):
    """Enumerates energy efficiency levels (also known as "classes" or "ratings") and certifications that are part of several international energy efficiency standards."""

    pass


class EUEnergyEfficiencyEnumeration(EnergyEfficiencyEnumeration):
    """Enumerates the EU energy efficiency classes A-G as well as A+, A++, and A+++ as defined in EU directive 2017/1369."""

    pass


class EnergyStarEnergyEfficiencyEnumeration(EnergyEfficiencyEnumeration):
    """Used to indicate whether a product is EnergyStar certified."""

    pass


class PostalAddress(ContactPoint):
    """
    The mailing address.
    """

    addressCountry: Union[Literal, "Country"]  # The country of the address
    addressLocality: Literal  # The locality of the address, e.g. city or town
    addressRegion: Literal  # The region of the address, e.g. state or province
    postOfficeBoxNumber: Literal  # The post office box number of the address
    postalCode: Literal  # The postal code of the address
    streetAddress: Literal  # The street address of the location
    extendedAddress: Literal  # An extended address, e.g. apartment or suite number


class Schedule(Intangible):
    """
    A schedule defines a repeating time period used to describe a regularly occurring Event. At a minimum a schedule will specify repeatFrequency which describes the interval between occurrences of the event. Additional information can be provided to specify the schedule more precisely. This includes identifying the day(s) of the week or month when the recurring event will take place, in addition to its start and end time. Schedules may also have start and end dates to indicate when they are active, e.g. to define a limited calendar of events.
    """

    byDay: Union["DayOfWeek", Literal]
    byMonth: Literal
    byMonthDay: Literal
    byMonthWeek: Literal
    duration: Union["Duration", "QuantitativeValue"]  # The duration of the schedule
    endDate: Literal  # The end date of the schedule
    endTime: Literal  # The end time of the schedule
    exceptDate: Literal  # Dates when the schedule does not apply
    repeatCount: Literal  # The number of times the schedule repeats
    repeatFrequency: Union[
        "Duration", Literal
    ]  # The frequency of the schedule, e.g. every 2 weeks
    scheduleTimezone: Literal  # The timezone of the schedule, e.g. 'America/New_York'
    startDate: Literal  # The start date of the schedule
    startTime: Literal  # The start time of the schedule


class MeasurementTypeEnumeration(Enumeration):
    """
    This term is in the "new" area - implementation feedback and adoption from applications and websites can help improve our definitions.
    """

    valueReference: Union["PropertyValue", "QualitativeValue", "QuantitativeValue"]


class QualitativeValue(Enumeration):
    """
    A predefined value for a product characteristic, e.g. the power cord plug type 'US' or the garment sizes 'S', 'M', 'L', and 'XL'.
    """

    additionalProperty: "PropertyValue"
    equal: "QualitativeValue"
    greater: "QualitativeValue"
    greaterOrEqual: "QualitativeValue"
    lesser: "QualitativeValue"
    lesserOrEqual: "QualitativeValue"
    nonEqual: "QualitativeValue"
    valueReference: Union[
        "DefinedTerm",
        Enumeration,
        MeasurementTypeEnumeration,
        "PropertyValue",
        "QualitativeValue",
        "QuantitativeValue",
        "StructuredValue",
        Literal,
    ]


class DayOfWeek(Enumeration):
    """
    Enumeration of the days of the week.
    """

    businessDays: Union["ServicePeriod", "ShippingDeliveryTime"]
    byDay: Schedule
    dayOfWeek: Union["EducationalOccupationalProgram", OpeningHoursSpecification]


class SizeSystemEnumeration(Enumeration):
    """
    Enumerates common size systems for different categories of products, for example "EN-13402" or "UK" for wearables or "Imperial" for screws.
    """

    pass


class SizeSpecification(QualitativeValue):
    """
    Size related properties of a product, typically a size code (name) and optionally a sizeSystem, sizeGroup, and product measurements (hasMeasurement). In addition, the intended audience can be defined through suggestedAge, suggestedGender, and suggested body measurements (suggestedMeasurement).
    """

    hasMeasurement: "QuantitativeValue"
    sizeGroup: Union[
        Literal, "SizeGroupEnumeration"
    ]  # The group to which the size belongs, e
    sizeSystem: Union[
        Literal, "SizeSystemEnumeration"
    ]  # The system used for the size, e.g. 'US', 'EU', 'UK'
    # suggestedAge: QuantitativeValue  # The suggested age for the size
    # suggestedGender: Union[Literal, "GenderType"]
    # suggestedMeasurement: QuantitativeValue  # Suggested body measurements for the size


class SizeGroupEnumeration(Enumeration):
    """
    Enumeration of size groups, such as 'petite', 'plus', 'tall', etc.
    """

    sizeGroup: SizeSpecification


class QuantitativeValue(StructuredValue):
    """
    A point value or interval for product characteristics and other purposes.
    """

    additionalProperty: "PropertyValue"
    maxValue: Literal
    minValue: Literal
    unitCode: Union[Literal, URIRef]  # The unit of measurement for the value
    unitText: Literal  # The unit of measurement as text
    value: Union[Literal, StructuredValue]  # The value of the property
    valueReference: Union[
        "DefinedTerm",
        Enumeration,
        MeasurementTypeEnumeration,
        "PropertyValue",
        "QualitativeValue",
        "QuantitativeValue",
        "StructuredValue",
        Literal,
    ]  # The value reference for the property


class ShippingDeliveryTime(StructuredValue):
    """
    A structured value providing information about the delivery time of a product or service.
    It can include additional information such as the shipping method, delivery time, and shipping destination.
    """

    businessDays: Union[
        "DayOfWeek", "OpeningHoursSpecification"
    ]  # The business days during which the delivery is available
    cutoffTime: Literal  # The cutoff time for the delivery
    handlingTime: Union[
        "QuantitativeValue", "ServicePeriod"
    ]  # The handling time for the delivery
    transitTime: Union[
        "QuantitativeValue", "ServicePeriod"
    ]  # The transit time for the delivery


class SchemaOrgClass(Intangible):
    """
    A class, also often called a 'Type'; equivalent to rdfs:Class.
    """

    _class_iri: URIRef = SCHEMAORG.Class
    supersededBy: Union["SchemaOrgClass", "SchemaOrgProperty", Enumeration]


class SchemaOrgProperty(Intangible):
    """
    A property, used to indicate attributes and relationships of some Thing; equivalent to rdf:Property.
    """

    _class_iri: URIRef = SCHEMAORG.Property
    domainIncludes: SchemaOrgClass
    inverseOf: "SchemaOrgProperty"
    rangeIncludes: SchemaOrgClass
    supersededBy: Union["SchemaOrgProperty", Enumeration, SchemaOrgClass]


class PropertyValue(StructuredValue):
    """
    A PropertyValue is a structured value that represents a property of an item.
    It can include additional information such as the unit of measurement or the value type.
    """

    maxValue: Literal
    minValue: Literal
    propertyID: Union[Literal, URIRef]
    unitCode: Union[Literal, URIRef]
    unitText: Literal
    value: Union[Literal, StructuredValue]
    valueReference: Union[
        DefinedTerm,
        Enumeration,
        MeasurementTypeEnumeration,
        "PropertyValue",
        QualitativeValue,
        QuantitativeValue,
        StructuredValue,
        Literal,
    ]
    # measuerementTechnique: Literal  # Optional technique used to measure the value
    # measurementMethod: Literal  # Optional method used to measure the value


class Brand(Intangible):
    """
    A brand is a name used by an organization or business person for labeling a product, product group, or similar.
    """

    # aggregateRating: "AggregateRating"  # An aggregate rating of the item
    logo: Union[URIRef, ImageObject]  # The logo of the brand
    # review: "Review"  # A review of the brand
    slogan: Literal  # A slogan associated with the brand


class VirtualLocation(Intangible):
    """
    An online or virtual location for attending events. For example, one may attend an online seminar or educational event. While a virtual location may be used as the location of an event, virtual locations should not be confused with physical locations in the real world.
    """

    pass


class Organization(Thing):
    """
    An organization such as a school, NGO, corporation, club, etc.
    """

    # acceptedPaymentMethod: Union["PaymentMethod", "LoanOrCredit", Literal]  # The payment methods accepted by the organization
    # actionableFeedbackPolicy: Union[URIRef, "CreativeWork"]  # The policy for actionable feedback from users
    address: Union[PostalAddress, Literal]  # The address of the organization
    # aggregateRating: "AggregateRating"  # An aggregate rating of the organization
    # alumni: Person
    areaServed: Union[
        Literal, "Place", "AdministrativeArea", GeoShape
    ]  # The area served by the organization
    award: Literal  # An award won by the organization
    brand: Union[Brand, "Organization"]  # The brand associated with the organization
    companyRegistration: "Certification"
    ContactPoint: ContactPoint  # A contact point for the organization
    # correctionsPolicy: Union[URIRef, "CreativeWork"]  # The corrections policy of the organization
    department: "Organization"  # A department within the organization
    dissolutionDate: Literal  # The date when the organization was dissolved
    # diversityPolicy: Union[URIRef, "CreativeWork"]  # The diversity policy of the organization
    # diversityStaffingReport: Union[URIRef, "CreativeWork"]  # The diversity staffing report of the organization
    duns: (
        Literal  # The Data Universal Numbering System (DUNS) number of the organization
    )
    email: Literal  # The email address of the organization
    # employee: Person
    # ethicsPolicy: Union[URIRef, "CreativeWork"]  # The ethics policy of the organization
    # event: Event
    faxNumber: Literal  # The fax number of the organization
    # founder: Union["Person", "Organization"]  # The founder(s) of the organization
    foundingDate: Literal  # The date when the organization was founded
    foundingLocation: Union[
        "Place", "AdministrativeArea", GeoShape
    ]  # The location where the organization was founded
    # funding: Grant
    globalLocationNumber: (
        Literal  # The Global Location Number (GLN) of the organization
    )
    hasCertification: "Certification"  # Certification details for the organization
    # hasCredentials: "EducationalOccupationalCredential"  # Credentials held by the organization
    hasGS1DigitalLink: URIRef  # The GS1 Digital Link for the organization
    # hasMemberProgram: MemberProgram
    # hasMerchantReturnPolicy: "MerchantReturnPolicy"  # The return policy of the organization
    # hasOfferCatalog: "OfferCatalog"  # The catalog of offers provided by the organization
    hasPOS: "Place"
    # hasShippingService: "ShippingService"  # The shipping service provided by the organization
    # interactionStatistic: "InteractionCounter"  # Statistics about interactions with the organization
    isicV4: Literal  # The International Standard Industrial Classification (ISIC) code for the organization
    iso6523Code: Literal  # The ISO 6523 code for the organization
    keywords: Union[
        Literal, "DefinedTerm", URIRef
    ]  # Keywords associated with the organization
    knowsAbout: Union[
        "Thing", Literal, URIRef
    ]  # Topics the organization is knowledgeable about
    knowsLanguage: Union[Literal, "Language"]  # Languages spoken by the organization
    legalAddress: PostalAddress  # The legal address of the organization
    legalName: Literal  # The legal name of the organization
    leiCode: Literal  # The Legal Entity Identifier (LEI) code of the organization
    location: Union[
        "Place", "PostalAddress", Literal, "VirtualLocation"
    ]  # The location of the organization
    logo: Union[URIRef, ImageObject]  # The logo of the organization
    # makesOffer: Offer # Offers made by the organization
    # member: Union["Person", "Organization"]  # Members of the organization
    # memberOf: Union["Organization", "ProgramMembership", "MemberProgramTier"]  # The organization to which this organization belongs
    naics: Literal  # The North American Industry Classification System (NAICS) code for the organization
    # nonprofitStatus: "NonprofitType"  # The nonprofit status of the organization
    # numberOfEmployees: "QuantitativeValue"  # The number of employees in the organization
    # owns: Union["Product", "OwnershipInfo"]  # Products or assets owned by the organization
    parentOrganization: "Organization"  # The parent organization of this organization
    # publishingPrinciples: Union[URIRef, "CreativeWork"]  # The publishing principles of the organization
    # review: "Review"  # Reviews or aggregate ratings of the organization
    # seeks: Demand
    skills: Union[
        Literal, "DefinedTerm"
    ]  # Skills or expertise offered by the organization
    slogan: Literal  # Slogans associated with the organization
    # sponsor: Union["Person", "Organization"]  # A sponsor of the organization
    subOrganization: "Organization"  # A sub-organization within the organization
    taxID: Literal  # The tax identification number of the organization
    telephone: Literal  # The telephone number of the organization
    # unnamedSourcesPolicy: Union[URIRef, "CreativeWork"]  # The policy regarding unnamed sources of information
    vatID: (
        Literal  # The Value Added Tax (VAT) identification number of the organization
    )


class Person(Thing):
    """
    A person (alive, dead, undead, or fictional).
    """

    address: Union[PostalAddress, Literal]  # The address of the person
    affiliation: "Organization"  # The organization the person is affiliated with
    brand: Union[Brand, Organization]  # The brand associated with the person
    contactPoint: ContactPoint  # A contact point for the person
    email: Literal  # The email address of the person
    familyName: Literal  # The family name of the person
    givenName: Literal  # The given name of the person
    faxNumber: Literal  # The fax number of the person
    # gender: Union[Literal, "GenderType"]  # The gender of the person
    hasCertification: Certification  # Certification details for the person
    jobTitle: Union["DefinedTerm", Literal]  # The job title of the person
    telephone: Literal  # The telephone number of the person
    workLocation: Union[
        "ContactPoint", "Place"
    ]  # The work location of the person, e.g. an office or a home office
    worksFor: "Organization"  # The organization the person works for


class Product(Thing):
    """
    Any offered product or service. For example: a pair of shoes; a concert ticket; the rental of a car; a haircut; or an episode of a TV show streamed online.
    """

    additionalProperty: Union[PropertyValue]
    # aggregateRating: "AggregateRating"  # An aggregate rating of the product
    asin: Union[
        Literal, URIRef
    ]  # The Amazon Standard Identification Number (ASIN) of the product
    # audience: Audience
    award: Literal  # An award won by the product
    brand: Union[Brand, Organization]  # The brand of the product
    category: Union["CategoryCode", Literal, Thing, URIRef, "PhysicalActivityCategory"]
    color: Literal  # The color of the product
    colorSwatch: Union[URIRef, ImageObject]  # A color swatch image of the product
    countryOfAssembly: Literal
    countryOfLastProcessing: Literal
    countryOfOrigin: "Country"
    depth: Union["Distance", "QuantitativeValue"]  # The depth of the product
    # funding: Grant
    gtin: Union[Literal, URIRef]  # The Global Trade Item Number (GTIN) of the product
    gtin12: Literal  # The GTIN-12 of the product
    gtin13: Literal  # The GTIN-13 of the product
    gtin14: Literal  # The GTIN-14 of the product
    gtin8: Literal  # The GTIN-8 of the product
    # hasAdultConsideration: "AdultConsideration"  # Considerations for adult content
    hasCertification: "Certification"
    hasEnergyConsumptionDetails: "EnergyConsumptionDetails"  # Details about the energy consumption of the product
    hasGS1DigitalLink: URIRef  # The GS1 Digital Link for the product
    hasMeasurement: QuantitativeValue
    # hasMerchantReturnPolicy: "MerchantReturnPolicy"  # The return policy of the merchant for the product
    height: Union["Distance", "QuantitativeValue"]  # The height of the product
    inProductGroupWithID: Literal  # The product group ID
    inAccessoryOrSparePartFor: "Product"  # The product or service that this product is an accessory or spare part for
    isConsumableFor: (
        "Product"  # The product or service that this product is a consumable for
    )
    isFamilyFriendly: Literal  # Indicates if the product is family-friendly
    isRelatedTo: Union["Product", "Service"]  # Related products or services
    isSimilarTo: Union["Product", "Service"]  # Similar products or services
    isVariantOf: Union[
        "ProductGroup", "ProductModel"
    ]  # The product or service that this product is a variant of
    itemCondition: "OfferItemCondition"  # The condition of the product
    keyword: Union[
        Literal, "DefinedTerm", URIRef
    ]  # Keywords associated with the product
    logo: Union[URIRef, ImageObject]  # The logo of the product
    manufacturer: Organization  # The manufacturer of the product
    material: Union[Literal, "Product", URIRef]  # The material of the product
    mobileUrl: Literal  # The mobile URIRef of the product
    model: Union[Literal, "ProductModel"]  # The model of the product
    mpn: Literal  # The Manufacturer Part Number (MPN) of the product
    # negativeNotes: Union["ItemList", "ListItem", Literal, "WebContent"]  # Negative notes about the product
    nsn: Literal  # The National Stock Number (NSN) of the product
    # offers: Union["Offer", "Demand"]  # The offers available for the product
    pattern: Union[Literal, DefinedTerm]  # The pattern of the product
    # positiveNotes: Union["ItemList", "ListItem", Literal, "WebContent"]  # Positive notes about the product
    productID: Literal
    productionDate: Literal  # The date of production of the product
    purchaseDate: Literal  # The date of purchase of the product
    releaseDate: Literal  # The release date of the product
    # review: "Review"  # A review or aggregate rating of the product
    size: Union[
        Literal, "SizeSpecification", "DefinedTerm", QuantitativeValue
    ]  # The size of the product
    sku: Literal  # The Stock Keeping Unit (SKU) of the product
    slogan: Literal  # A slogan associated with the product
    weight: Union["Mass", "QuantitativeValue"]  # The weight of the product
    width: Union["Distance", "QuantitativeValue"]  # The width of the product


class Place(Thing):
    """
    A Place is a specific location or area, such as a city, country, or building.
    It can include additional information such as the address, geographic coordinates, and opening hours.
    """

    address: Union["PostalAddress", Literal]  # The address of the place
    geo: Union["GeoCoordinates", "GeoShape"]  # The geographic coordinates of the place
    hasMap: URIRef  # A URIRef to a map of the place
    name: Literal  # The name of the place
    openingHours: Literal  # The opening hours of the place
    telephone: Literal  # The telephone number of the place


class AdministrativeArea(Place):
    """
    A geographical region, typically under the jurisdiction of a particular government
    """

    pass


class Country(AdministrativeArea):
    """
    A country
    """

    pass


class ProductGroup(Product):
    """
    A ProductGroup represents a group of Products that vary only in certain well-described ways, such as by size, color, material etc.

    While a ProductGroup itself is not directly offered for sale, the various varying products that it represents can be. The ProductGroup serves as a prototype or template, standing in for all of the products who have an isVariantOf relationship to it. As such, properties (including additional types) can be applied to the ProductGroup to represent characteristics shared by each of the (possibly very many) variants. Properties that reference a ProductGroup are not included in this mechanism; neither are the following specific properties variesBy, hasVariant, url.
    """

    hasVariant: Product
    productGroupID: Literal  # The ID of the product group
    variesBy: Union[
        Literal, "DefinedTerm"
    ]  # The attribute by which the products in the group vary


class ProductModel(Product):
    """
    A datasheet or vendor specification of a product (in the sense of a prototypical description).
    """

    isVariantOf: Union[
        ProductGroup, "ProductModel"
    ]  # The product group or model that this product is a variant of
    predecessorOf: "ProductModel"  # The predecessor product model or group
    successorOf: "ProductModel"  # The successor product model or group
