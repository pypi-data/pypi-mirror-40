# AWS-360-API

A Python Flask API used in AWS-360

## Install

```shell
pip install aws-360-api
```

## Endpoints

### `/heartbeat`

Returns with `200` if the application is healthy

* Example:

```json
{
  "msg": "I am an healthy flask app",
  "status": "success",
  "time": "2018-09-24 22:17:38.212565"
}
```

### `/info`

Returns with `200` with application information

* Example:

```json
{
  "git_revision": null,
  "git_tag": null,
  "server_name": "flask-api-alb-public-1654579006.us-east-1.elb.amazonaws.com"
}
```

### `/badge`

Returns a badge (![badge](https://img.shields.io/badge/style-plastic-green.svg?longCache=true&style=plastic))

* Params:
    * `name`: Name of the badge
    * `percent`: Percentage on the right hand side
    * `type`: [`json` or `html`]

```json
$ <api-endpoint>/badge?name=ccm&percent=95&type=json
```

![badge](https://img.shields.io/badge/style-plastic-green.svg?longCache=true&style=plastic)

```json
$ <api-endpoint>/badge?name=ccm&percent=95&type=json
{
  "svg": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"77\" height=\"20\">\n    <linearGradient id=\"b\" x2=\"0\" y2=\"100%\">\n        <stop offset=\"0\" stop-color=\"#bbb\" stop-opacity=\".1\"/>\n        <stop offset=\"1\" stop-opacity=\".1\"/>\n    </linearGradient>\n    <mask id=\"a\">\n        <rect width=\"77\" height=\"20\" rx=\"3\" fill=\"#fff\"/>\n    </mask>\n    <g mask=\"url(#a)\">\n        <path fill=\"#555\" d=\"M0 0h31v20H0z\"/>\n        <path fill=\"#4c1\" d=\"M31 0h46v20H31z\"/>\n        <path fill=\"url(#b)\" d=\"M0 0h77v20H0z\"/>\n    </g>\n    <g fill=\"#fff\" text-anchor=\"middle\" font-family=\"DejaVu Sans,Verdana,Geneva,sans-serif\" font-size=\"11\">\n        <text x=\"16.5\" y=\"15\" fill=\"#010101\" fill-opacity=\".3\">ccm</text>\n        <text x=\"15.5\" y=\"14\">ccm</text>\n    </g>\n    <g fill=\"#fff\" text-anchor=\"middle\" font-family=\"DejaVu Sans,Verdana,Geneva,sans-serif\" font-size=\"11\">\n        <text x=\"55.0\" y=\"15\" fill=\"#010101\" fill-opacity=\".3\">95.0</text>\n        <text x=\"54.0\" y=\"14\">95.0</text>\n    </g>\n</svg>"
}
```

### `/scrappe`

Parses an HTML body and extract `img` HTML tags from a url

* Params:
    * `url`: Valid URL to a website

```json
$ <api-endpoint>/scrappe?url=https://github.com

{
  "hit": 34,
  "imgs": [
    {
      "src": "https://assets-cdn.github.com/images/search-shortcut-hint.svg"
    },
    {
      "src": "https://assets-cdn.github.com/images/spinners/octocat-spinner-128.gif"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/building-the-future/green-purple-hexagons.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/airbnb-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/sap-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/ibm-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/google-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/paypal-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/bloomberg-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/spotify-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/swift-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/facebook-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/node-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/nasa-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/logos/walmart-logo.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/home-illo-team.svg"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/home-illo-team-code.svg"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/home-illo-team-chaos.svg"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/home-illo-team-tools.svg"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/home-illo-business.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/integrators/slackhq.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/integrators/zenhubio.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/integrators/travis-ci.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/integrators/atom.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/integrators/circleci.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/integrators/google.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/integrators/codeclimate.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/stories/developers/ariya.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/stories/developers/freakboy3742.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/stories/customers/mailchimp.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/stories/developers/kris-nova.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/stories/developers/yyx990803.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/stories/customers/mapbox.png"
    },
    {
      "src": "https://assets-cdn.github.com/images/modules/site/stories/developers/jessfraz.png"
    }
  ],
  "status": "success"
}
```


Made with ♥ for teaching people
