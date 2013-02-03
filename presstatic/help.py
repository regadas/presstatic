from string import Template

s3_setup = Template("""
Go to https://console.aws.amazon.com/s3 select your bucket and
add a bucket policy. Here's an example:

{
  "Version":"2008-10-17",
  "Statement":[{
    "Sid":"AddPerm",
        "Effect":"Allow",
      "Principal": {
            "AWS": "*"
         },
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::$bucket/*"
      ]
    }
  ]
}

For more info you should see:
http://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html
""").substitute