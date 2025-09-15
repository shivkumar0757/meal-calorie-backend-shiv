# USDA FoodData Central API Reference

## 📌 Overview

This document provides comprehensive information on using the USDA FoodData Central API for food and nutrient data retrieval in the Meal Calorie Backend project.

---

## 🔗 API Details

- **Base URL:** `https://api.nal.usda.gov/fdc/v1/`
- **API Documentation:** [https://fdc.nal.usda.gov/api-guide](https://fdc.nal.usda.gov/api-guide)
- **API Key Signup:** [https://fdc.nal.usda.gov/api-key-signup.html](https://fdc.nal.usda.gov/api-key-signup.html)
- **API Specification:** [https://fdc.nal.usda.gov/api-spec/fdc_api.html](https://fdc.nal.usda.gov/api-spec/fdc_api.html)

---

## 🔑 Authentication

The API uses API key authentication passed as a query parameter.

**Your API Key:** `your_actual_api_key_here`

⚠️ **Security Note:** Never commit your API key to version control. Use environment variables.

---

## 🔍 Food Search Endpoint

### Basic Search

**Endpoint:** `GET /foods/search`

**Parameters:**
- `query` (required) - Search term for food items
- `api_key` (required) - Your API key
- `pageSize` (optional) - Number of results to return (default: 50, max: 200)
- `pageNumber` (optional) - Page number for pagination (default: 1)
- `dataType` (optional) - Filter by data type (e.g., "Foundation", "Survey")

### Example cURL Requests

```bash
# Basic search for "chicken biryani"
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=chicken%20biryani&api_key=$USDA_API_KEY"

# Limit results to 5 items
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=chicken%20biryani&api_key=$USDA_API_KEY&pageSize=5"

# Search for "paneer" with specific data type
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=paneer&api_key=$USDA_API_KEY&dataType=Foundation"

# Search with pagination
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=rice&api_key=$USDA_API_KEY&pageSize=10&pageNumber=2"
```

### Example Response Structure

```json
{
  "totalHits": 1234,
  "currentPage": 1,
  "totalPages": 25,
  "pageList": [1, 2, 3, 4, 5],
  "foodSearchCriteria": {
    "query": "chicken biryani",
    "generalSearchInput": "chicken biryani",
    "pageNumber": 1,
    "pageSize": 50,
    "requireAllWords": false
  },
  "foods": [
    {
      "fdcId": 123456,
      "description": "Chicken biryani",
      "dataType": "Survey (FNDDS)",
      "publicationDate": "2021-10-28",
      "foodNutrients": [
        {
          "nutrientId": 1008,
          "nutrientName": "Energy",
          "nutrientNumber": "208",
          "unitName": "kcal",
          "value": 280.5
        },
        {
          "nutrientId": 1003,
          "nutrientName": "Protein",
          "nutrientNumber": "203",
          "unitName": "g",
          "value": 12.8
        }
      ]
    }
  ]
}
```

---

## 🍽️ Food Details Endpoint

### Get Specific Food Details

**Endpoint:** `GET /food/{fdcId}`

```bash
# Get details for specific food ID
curl "https://api.nal.usda.gov/fdc/v1/food/123456?api_key=$USDA_API_KEY"

# Get details with specific nutrients only
curl "https://api.nal.usda.gov/fdc/v1/food/123456?api_key=$USDA_API_KEY&nutrients=208,203,204,205"
```

---

## 🔧 Advanced Search (POST Method)

For more complex queries, use POST method:

```bash
curl -X POST "https://api.nal.usda.gov/fdc/v1/foods/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "chicken biryani",
    "pageSize": 5,
    "pageNumber": 1,
    "dataType": ["Survey (FNDDS)", "Foundation"],
    "nutrients": [208, 203, 204, 205]
  }' \
  --url "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=$USDA_API_KEY"
```

---

## 🧪 Testing Commands

### Quick Test Commands

```bash
# Test API connectivity
curl -f "https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&api_key=$USDA_API_KEY&pageSize=1"

# Test with Indian cuisine
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=dal&api_key=$USDA_API_KEY&pageSize=3"

# Test with common dishes
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=pizza&api_key=$USDA_API_KEY&pageSize=3"
```

---

## 📊 Key Nutrients

Common nutrient IDs you'll encounter:

| Nutrient ID | Name | Unit |
|-------------|------|------|
| 1008 | Energy (Calories) | kcal |
| 1003 | Protein | g |
| 1004 | Total lipid (fat) | g |
| 1005 | Carbohydrate, by difference | g |
| 1079 | Fiber, total dietary | g |
| 1087 | Calcium, Ca | mg |
| 1089 | Iron, Fe | mg |
| 1162 | Vitamin C, total ascorbic acid | mg |

---

## ⚡ Rate Limits

- **Rate Limit:** 1000 requests per hour per API key
- **Burst Limit:** 10 requests per second

---

## 🛠️ Best Practices

### For Development

1. **Environment Variables:**
   ```bash
   export USDA_API_KEY=$USDA_API_KEY
   curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=rice&api_key=$USDA_API_KEY"
   ```

2. **Error Handling:**
   ```bash
   # Test error response
   curl -f "https://api.nal.usda.gov/fdc/v1/foods/search?query=&api_key=$USDA_API_KEY" || echo "API Error"
   ```

3. **Response Validation:**
   ```bash
   # Pipe to jq for JSON validation
   curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&api_key=$USDA_API_KEY&pageSize=1" | jq .
   ```

### For Production

- Always use HTTPS
- Implement retry logic with exponential backoff
- Cache responses appropriately (respect API rate limits)
- Monitor API usage and implement graceful degradation
- Use connection pooling for better performance

---

## 🔍 Common Use Cases

### 1. Calorie Lookup
```bash
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=chicken%20breast&api_key=$USDA_API_KEY&pageSize=5" | jq '.foods[0].foodNutrients[] | select(.nutrientId == 1008)'
```

### 2. Macronutrient Profile
```bash
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=quinoa&api_key=$USDA_API_KEY&pageSize=1" | jq '.foods[0].foodNutrients[] | select(.nutrientId == 1008 or .nutrientId == 1003 or .nutrientId == 1004 or .nutrientId == 1005)'
```

### 3. Multiple Food Search
```bash
for food in "rice" "dal" "roti"; do
  echo "=== $food ==="
  curl -s "https://api.nal.usda.gov/fdc/v1/foods/search?query=$food&api_key=$USDA_API_KEY&pageSize=1" | jq -r '.foods[0].description // "Not found"'
done
```

---

## 📋 Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 400 | Bad Request | Check query parameters |
| 401 | Unauthorized | Verify API key |
| 403 | Forbidden | Check rate limits |
| 404 | Not Found | Verify endpoint URL |
| 429 | Too Many Requests | Implement rate limiting |
| 500 | Internal Server Error | Retry with exponential backoff |

---

## 📚 Additional Resources

- [USDA FoodData Central](https://fdc.nal.usda.gov)
- [API Documentation](https://fdc.nal.usda.gov/api-guide)
- [Dataset Downloads](https://fdc.nal.usda.gov/download-datasets)
- [Postman Collection](https://www.postman.com/api-evangelist/agricultural-research-service-ars/documentation/nex4lq6/food-data-central-api)
