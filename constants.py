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
  "project_id": "refined-analogy-416813",
  "private_key_id": "15be7e2f72a6870e24996ee39747a87831de1011",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDVxCiGB9Lg+c1Q\nmr9/4pD0PeTgpMv4Qz0QSaUQOy9Co7SjY5d6AQsMJWGYQXZ1Wjc7p97oY9PyIroB\nnbH65k6M6PW42y6sjop6wYkHBnpE0rPS3+fHcOcvdzz4SGf2rT+oRItei37LqCc4\ns3hqriyl4Hpw7Du9FuZX+OsfEMJx3/ZEK8OSsHNsv0fQysp8jhZL11PwuYkznIZC\nXbTKgzP6VhvZMPNCQ8bcbR3t9Cjgx0tX0QUduplaep+biEqXk+Mzq6jLl281K1ah\nRciUQCzG4Uh27h9IZULtjq3dYQNu07mfYq0Z1qXNM09oXCnC0Dz1/27ZCX/HLeKh\nbXL3OaV9AgMBAAECggEAATHhREnLXIyncgA2V4mbb4oOqcTJURSFULh9wDP5k7Je\n08rKCOr0Hs8flwckGWkBdHvFl2vCstZfIG1G0KC0eINvMxX/o75G8z20gzw4znas\nrF41wJYLBAo4/Zyl/wZ7J3jC+WS42dmRW0henipl4k7txKO5wfAia752H293Ua4S\nfz59fHztGb1/FztWG9nj/iJX+fy5RDNBBhsTZbkHkfEUgyxORNVmwSc8kC6HEr4+\nT/Fsz2vUpwvmIyDcqJ2Ib/5rnwxcYWubm3z9N6Y842Ew2tBdIv0rYhd5qCV5u5Z4\n8qEbKash6KhlfKR3gBCDEEaFa21oSO9mVhb4nlf8HwKBgQDqgEBudmZ2UsS43yeO\nJ/VsiMRAzRJbmBvl4ZvAaLtxzNipXMvpp5WWk1SuFPPC64DqF6rqyX61emSVQ9R9\nMmqAXO+w5hDHybQAvlZepkMmQZ80R72MZPDWzC5leT0CXYKPv9GTtP7WqipVgx7M\nrO78Iw1oEOcgbuYwXbD9tekXXwKBgQDpXULojO2NVCM1plcb/S1vlOf8k6VpomGg\nGEMcpJI4HLVCiId6+VmxmO3QmYB9d1MsrM/3v5ExcBNvLf6ZwovKiQHua6dDephB\n1rOVEOYANlw/szbVmqf45HP+k/NsbF9/MD7wgpd+N6DXn/WRkoUjbjBXcGxFHwEl\nQ42VyRq8owKBgQDSY0prUJLQ6aVRb/SfF76bJ4Fb2iD0SF4POwBv+gbiLLTeDkFs\nWkxdEcXRgT7JzFyWqbFQgILL8wk22epUgN0IWVk6zs6TUKXMXPhEZsqsEgfx8cNf\nqFhjfkDKDaHs81Rl/+TZrnNMyNK+cas6WpT3ZcNrcG7MrHKdRhG7Lm/35QKBgQCc\n8xFl8Cpwi+7mTUp20480ZXSlBfQRGJoKH2c7o1+IB57M8aAU0BFIBa+kRSkKuS8i\nc9OnL5sKIfOgKdH7PcHg5MZ8wMCM/K3cUfcTwXq/F9BxMyok/VANcDCnPoBQIo8T\nrrIV9e7Hf8hYXQe+8UlD6/7tP/pBfrm5gzZ9T/UAewKBgExYmDadb+jlUx63qesX\nureeqiz+dlJJg6eyV1F2GaOSQCTJjGFRZ4j50/4298fIR4aqKkboijsPEjIvYyrS\nJ/YM158iKj69MFF/nW79u9w4srSiCSnSVEiaerOk7JxTQAZcAPLvLEZlRMpJbvOx\n4HvgWfMuD8NqQyMJBdZiVtdW\n-----END PRIVATE KEY-----\n",
  "client_email": "dummy-111@refined-analogy-416813.iam.gserviceaccount.com",
  "client_id": "116979646827856631028",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dummy-111%40refined-analogy-416813.iam.gserviceaccount.com",
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
