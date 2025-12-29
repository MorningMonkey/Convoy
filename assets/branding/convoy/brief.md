{
  "product": {
    "name": "Convoy",
    "slug": "convoy",
    "tagline": "Mission Control workspace for agentic development"
  },
  "paths": {
    "projectFactoryDir": "GAS_PROJECT",
    "docsDir": "docs",
    "scriptsDir": "scripts"
  },
  "defaults": {
    "language": "ja",
    "license": "ISC",
    "git": {
      "defaultBranch": "main"
    },
    "release": {
      "channel": "alpha",
      "versionPrefix": "v"
    }
  },
  "branding": {
    "voice": "clear, disciplined, safety-first",
    "styleKeywords": ["mission-control", "standardization", "automation"]
  },
  "safety": {
    "requireConfirmationForDestructiveOps": true,
    "neverCommitSecrets": true
  },
  "productId": "convoy",
  "factoryDir": "d:/convoy",

  "header": {
    "promptFile": "assets/branding/{productId}/header_prompt.txt",
    "input": "assets/header.png",
    "cropped": "assets/header_cropped.png",
    "final": "assets/header_cropped_text.png"
  }
}
