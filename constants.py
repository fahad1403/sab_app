import random

WEB_ANALYSIS_DATA = {
    "traffic": [
        {
            "date": "2023-01-01",
            "traffic": random.uniform(1000, 1500)
        },
        {
            "date": "2023-02-01",
            "traffic": random.uniform(1000, 1500)
        },
        {
            "date": "2023-03-01",
            "traffic": random.uniform(1000, 1500)
        },
        {
            "date": "2023-04-01",
            "traffic": random.uniform(1000, 1500)
        },
        {
            "date": "2023-05-01",
            "traffic": random.uniform(1000, 1500)
        },
        {
            "date": "2023-06-01",
            "traffic": random.uniform(1000, 1500)
        },
        {
            "date": "2023-07-01",
            "traffic": random.uniform(1000, 1500)
        },
        {
            "date": "2023-08-01",
            "traffic": random.uniform(1000, 1500)
        }
    ]
}

WEB_AVERAGE_DURATION_DATA = { "duration": [
    {
        "date": "2023-01-01",
        "average_visit_duration": random.uniform(200, 1000)
    },
    {
        "date": "2023-02-01",
        "average_visit_duration": random.uniform(200, 1000)
    },
    {
        "date": "2023-03-01",
        "average_visit_duration": random.uniform(200, 1000)
    },
    {
        "date": "2023-04-01",
        "average_visit_duration": random.uniform(200, 1000)
    },
    {
        "date": "2023-05-01",
        "average_visit_duration": random.uniform(200, 1000)
    },
    {
        "date": "2023-06-01",
        "average_visit_duration": random.uniform(200, 1000)
    },
    {
        "date": "2023-07-01",
        "average_visit_duration": random.uniform(200, 1000)
    },
    {
        "date": "2023-08-01",
        "average_visit_duration": random.uniform(200, 1000)
    }
]
}

device_id = str(random.randint(10000000, 99999999))

THM_RESPONSE = {
  "identity_verification": {
    "user_behavior_match": True,  # Generate a random boolean value
    "identity_verified": True  # Generate a random boolean value
  },
  "device_fingerprint": {
    "device_id": device_id  # Include the generated device ID
  },
  "geolocation": {
    "country": "Kingdom of Saudi Arabia",
    "latitude": round(random.uniform(-90, 90), 4),  # Generate a random latitude
    "longitude": round(random.uniform(-180, 180), 4)  # Generate a random longitude
  },
  "bot_detection": {
    "is_bot": False  # Generate a random boolean value
  }
}

GDRIVE_CREDS = {
    "type": "service_account",
    "project_id": "decisive-studio-400406",
    "private_key_id": "6b431804f09e3dbe36a2935c2608ce9f1f032d34",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdxe4MxX3rR1nd\nohrrVfK2NOdQt991SpHR3W1NgOg0qTYwbHzJdXYz4s1sTAqBfw06V9rFdcYaSOsU\nDC1zbJwLEHain0NiAalTJ75drcUJH8hRwwdgAMI0nuQchi9LcT0rNH41B7jCgY6d\n2o7qifBqOEcWhz+PI12tsYcF+qQT7fH84qErw0xzZaKQvOF7bieszjvrAQfEJsfD\nq3NA11ArIi2WQvwYtVz6Uo0Fl7vCP6W/c/JXsi38X2dZ0VUZDCoyUOIK87yxwSQf\nSZhY6HhXPkK5vC0b0gGRrvRhBcrMSC9fWqTEq4q6rOCbuFtpTlkpSYAj4z4w66Tr\nqT35R+llAgMBAAECggEAI8nzgSmmceG+UKB2R0Z4l1ziUOTY12gqMkcuhWt1oQZ2\nUJ83YlKXFNeAni2Un4HkzASET5Dy9mDulF5bzAhJ0Fe0dZi3hgqW8JI+JE1n+fUf\n8W4SZPRfGWUmnRLSNSSTidKvQ1PEVTji00tx6mGOa+XmuEVHRW6yEBXKaXCM2ikf\nH59rVxWSh5UF48qbhYePqtUn5NlTrQx/vPEoUFQWO8drrbm1BPkqFyh+GHy6fPKk\nQ4nVST+QwFiPKA3hqSeS0H7q7nx0z1gqfqV37s0r/NJQ/RUrvKnqbXQxx16FYtit\nstczn7Ot/8MYyENoRliRk5XzKwlTNkIm1k10l2c3MQKBgQDRYIZrb+jKBh/WyCxh\nWXV7EQgQL8zMrd0CJURBguG5h+QpZ1nNLC2NlfLrz+8fdjl/lf+y2fE/F9O7WVRr\nLpvRJoYphexgPr6R9zRw5B1K51z/zQQe1eO/4vVQLN+dxIJ6WU/LRQbc5pS6ve4+\nK143QnLfRkJH0cF1Ugy8oU6SNQKBgQDA572uZmvYm2eZi/MIkx+9PaFDleJPPKJz\ne9FvLxomciusWVogX8K9q9YExMQU3ZWResDcBYU2pqIyJToDiNbaCGrCEeV2XEnT\nnj57NNYDPBW8FEiyG+/DA0u71CiS33wHmB1T113ORtS5yCPzkI4ABK45sx3RTKsX\nK25vNF/gcQKBgBFEkbF4qE1JFgUjuy1IMH022WBkYNKcoDaWFjwE7FLd1z5m7KwU\nMamUrVUvb/w7RuCz4UPB37ihYW/5HRI95NHqCHSSO/1wD02Ags2wso3D6RKbuPRG\nFaN0t2CmYsbjNxOaHA+aoMdFKQ0Brw1njDyoeUraw4qizP69Bpnj/9PlAoGBAJmB\nD5DTUeiJKbSnCBt/r9cQTt6QTAlPr9oD4pH+QmnrmlNIuw5eBYKXVfRve7U66sVc\nkFHFVs85ZIJQ20xqvMW9wu5x/U3lfJ4YI5I5ZkAmtQj4fyy0TGO7oK1z02Gk03bb\nliLck3oNJUQ9PlaYZlcfYmDp5sVhpBgI6JU3cUARAoGAB1MHYJWxFgt95YF77wXX\ndSqa+Twz8z3/EGGSwXaLwdfOBhMRi2iqdWNO5jTbtRcVT1fSpATI5pJ1Z4IXSR48\nKrtpOKFKtPVluJPhB1ntjaCoL538xaBfLUJXUcZ1g+cGCSm5g7VqLOagUDOh/ryE\njYaGhYr8Zo1qp2UTYADFggI=\n-----END PRIVATE KEY-----\n",
    "client_email": "vision-creds-new@decisive-studio-400406.iam.gserviceaccount.com",
    "client_id": "101067322817118129247",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vision-creds-new%40decisive-studio-400406.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }


SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

import json

# JSON structure to be filled
CONTRACT_JSON_DATA = '''
{
  "contract": {
    "basicInfo": {
      "contractNumber": 0,
      "contractCopyNumber": 0,
      "contractDate": "string",
      "companyDuration": 0,
      "establishmentDate": "string",
      "companyAddress": "string"
    },
    "crInfo": {
      "crType": 0,
      "crTypeDescriptionAr": "string",
      "crNationalNo": "string",
      "crNo": "string",
      "companyFullName": "string",
      "headquartersCityId": 0,
      "headquartersCityNameAr": "string"
    },"companyForm": {
      "companyFormId": 0,
      "companyFormDescriptionAr": "string"
    },
    
    "activities": [
      {
        "activityId": "string",
        "activityDescriptionAr": "string",
        "isLicenseRequiredtoStart": true
      }
    ],
    "notifications": [
      {
        "notificationMethodId": 0,
        "notificationMethodDescriptionAr": "string",
        "otherText": "string"
      }
    ],
    "companyManagement": {
      "responsibleTypeId": 0,
      "responsibleTypeDescriptionAr": "string"
    },
    "partnerDecision": {
      "additionalDecisionText": "string",
      "decisions": [
        {
          "partnerDecisionId": 0,
          "partnerDecisionDescriptionAr": "string",
          "approvePercentage": 0,
          "approveAdditionalText": "string"
        }
      ]
    },
    "companyCapital": {
      "capital": 0,
      "capitalTypeId": 0,
      "capitalTypeDescriptionAr": "string",
      "cashCapital": 0,
      "inKindCapital": 0,
      "totalCashContribution": 0,
      "totalInKindContribution": 0,
      "contributionValue": 0,
      "cashContributionFulfilled": true,
      "daysToFulfilCashContribution": 0
    },
    "companyStockCapital": {
      "capital": 0,
      "capitalTypeId": 0,
      "capitalTypeDescriptionAr": "string",
      "cashCapital": 0,
      "inKindCapital": 0,
      "announcedCapital": 0,
      "padiCapital": 0,
      "bankId": 0,
      "bankDescriptionAr": "string"
    },
    "fiscalYear": {
      "calendarTypeId": 0,
      "calendarTypeDescriptionAr": "string",
      "fiscalYearEndMonth": 0,
      "fiscalYearEndDay": 0,
      "fiscalYearEndYear": 0
    },
    "profitLossDistribution": {
      "setasidepercentage": 0,
      "sideProfitPercentage": "string",
      "sideProfitPurpose": "string"
    },
    "expenses": [
      {
        "statement": "string",
        "value": 0
      }
    ],
    "stocks": [
      {
        "stockClassNameAr": "string",
        "stockTypeDescriptionAr": "string",
        "stockClassRights": "string",
        "stockCount": 0,
        "stockValue": 0,
        "additionalText": "string"
      }
    ]
  },
  "partners": {
    "individualsPartners": [
      {
        "partnerTypeId": 0,
        "partnerTypeDescriptionAr": "string",
        "partnershipTypeId": 0,
        "partnershipTypeDescriptionAr": "string",
        "partnerBasicInfo": {
          "identifierNo": "string",
          "identifierTypeId": 0,
          "identifierTypeDescriptionAr": "string",
          "firstNameAr": "string",
          "fatherNameAr": "string",
          "grandFatherNameAr": "string",
          "familyNameAr": "string",
          "birthDate": "string",
          "profession": "string",
          "genederId": 0,
          "genderDescriptionAr": "string",
          "nationalityId": 0,
          "nationalityDescriptionAr": "string",
          "minor": true,
          "incapacitated": true
        },
        "capitalPartnerShare": {
          "cashContribution": 0,
          "inkindContribution": 0,
          "totalContribution": 0
        },
        "stockPartnerShare": [
          {
            "stockTypeId": 0,
            "stockTypeDescriptionAr": "string",
            "stockClassDescriptionAr": "string",
            "stockShareCount": 0
          }
        ],
        "partnerProfitLossDistribution": {
          "profitPercentage": 0,
          "lossPercentage": 0
        },
        "misaLicenseNo": "string"
      },
      {
        "partnerTypeId": 0,
        "partnerTypeDescriptionAr": "string",
        "partnershipTypeId": 0,
        "partnershipTypeDescriptionAr": "string",
        "partnerBasicInfo": {
          "identifierNo": "string",
          "identifierTypeId": 0,
          "identifierTypeDescriptionAr": "string",
          "firstNameAr": "string",
          "fatherNameAr": "string",
          "grandFatherNameAr": "string",
          "familyNameAr": "string",
          "birthDate": "string",
          "profession": "string",
          "genederId": 0,
          "genderDescriptionAr": "string",
          "nationalityId": 0,
          "nationalityDescriptionAr": "string",
          "minor": true,
          "incapacitated": true
        },
        "guardian": {
          "identifierTypeId": "string",
          "identifierTypeDescriptionAr": 0,
          "identifierNo": "string",
          "firstNameAr": "string",
          "fatherNameAr": "string",
          "grandFatherNameAr": "string",
          "familyNameAr": "string",
          "birthDate": "string",
          "genederId": 0,
          "genderDescriptionAr": "string",
          "nationalityId": 0,
          "nationalityDescriptionAr": "string",
          "isFatherGuardian": true
        },
        "capitalPartnerShare": {
          "cashContribution": 0,
          "inkindContribution": 0,
          "totalContribution": 0
        },
        "stockPartnerShare": [
          {
            "stockTypeId": 0,
            "stockTypeDescriptionAr": "string",
            "stockClassDescriptionAr": "string",
            "stockShareCount": 0
          }
        ],
        "partnerProfitLossDistribution": {
          "profitPercentage": 0,
          "lossPercentage": 0
        },
        "misaLicenseNo": "string"
      }
    ],
    "companyPartners": [
      {
        "partnerTypeId": 0,
        "partnerTypeDescriptionAr": "string",
        "partnershipTypeId": 0,
        "partnershipTypeDescriptionAr": "string",
        "companyBasicInfo": {
          "identifierTypeId": 0,
          "identifierTypeDescriptionAr": "string",
          "crNationalNo": "string",
          "companyNameAr": "string",
          "companyFormID": 0,
          "companyFormDescriptionAr": "string"
        }
      }
    ],
    "establishmentPartners": [
      {
        "partnerTypeId": 0,
        "partnerTypeDescriptionAr": "string",
        "partnershipTypeId": 0,
        "partnershipTypeDescriptionAr": "string",
        "establishmentBasicInfo": {
          "identifierTypeID": 0,
          "identifierTypeDescriptionAr": "string",
          "crNationalNo": "string",
          "establishmentNameAr": "string"
        }
      }
    ],
    "endowmentPartners": [
      {
        "partnerTypeId": 0,
        "partnerTypeDescriptionAr": "string",
        "partnershipTypeId": 0,
        "partnershipTypeDescriptionAr": "string",
        "stockPartnerShare": "string",
        "realAssets": [
          {}
        ],
        "partnerEndowmentBasicInfo": {
          "identifierTypeId": 0,
          "identifierTypeDescriptionAr": "string",
          "deedNo": "string",
          "deedIssueDate": "string",
          "deedIssueDateHijri": "string",
          "endowmentNameAr": "string"
        },
        "capitalPartnerShare": {
          "cashContribution": 0,
          "inkindContribution": 0,
          "totalContribution": 0
        },
        "partnerProfitLossDistribution": {
          "profitPercentage": 0,
          "lossPercentage": 0
        }
      }
    ]
  },
  "managers": [
    {
      "managerBasicInfo": {
        "identifierTypeId": 0,
        "identifierTypeDescriptionAr": "string",
        "identifierNo": "string",
        "firstNameAr": "string",
        "fatherNameAr": "string",
        "grandFatherNameAr": "string",
        "familyNameAr": "string",
        "birthDate": "string",
        "genderId": 0,
        "genderDescriptionAr": "string",
        "nationalityId": 0,
        "nationalityDescriptionAr": "string",
        "isPartner": true,
        "managerPositionID": 0,
        "managerPositionDescriptionAr": "string",
        "managerPositionDescriptionEn": "string"
      }
    }
  ]
}
'''
