# 🛡️ WAF and Shield

## 🧠 What is AWS WAF?
AWS WAF (Web Application Firewall) helps protect web applications from common web exploits such as SQL injection and cross-site scripting.

### Common WAF use cases
- protect public web applications
- filter requests based on IP, headers, or URI strings
- block bots or suspicious traffic

---

## 🧠 What is AWS Shield?
AWS Shield is a managed DDoS protection service. It helps protect applications from distributed denial-of-service attacks.

### Shield tiers
- Shield Standard: available automatically for many AWS services
- Shield Advanced: enhanced protection for critical applications

---

## 🔄 WAF vs Shield
- WAF protects at the application layer using rules
- Shield protects against DDoS attacks
- They are often used together for stronger protection

---

## 🧪 Practical Part

### 1. 🛠️ Manual labs
#### Lab 1: Create a WAF rule
1. Open the WAF console.
2. Create a web ACL.
3. Add a rule to block requests from a specific IP or suspicious pattern.
4. Associate the ACL with an Application Load Balancer or CloudFront distribution.
5. Test the rule by sending a request.

Expected result: requests matching the rule are blocked.

#### Lab 2: Review Shield protection
1. Open the Shield console.
2. Review the protection status of your resources.
3. Confirm whether Standard or Advanced protection is enabled.

Expected result: students understand how DDoS protection is applied.

### 2. 🧱 Terraform example
```hcl
resource "aws_wafv2_web_acl" "demo" {
  name        = "demo-web-acl"
  scope       = "REGIONAL"
  description = "Example web ACL"

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "demo-web-acl"
    sampled_requests_enabled   = true
  }
}
```

---

## 📝 Exam Notes
- WAF protects web applications from common attacks.
- Shield protects against DDoS traffic.
- Both are important for application security.