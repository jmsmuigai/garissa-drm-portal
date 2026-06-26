#!/bin/bash

# ==============================================================
# GARISSA DRM - GCP AGENT PLATFORM ENABLER
# ==============================================================
# This script enables all required Google Cloud APIs for the Agent 
# Garden Platform so that Gemini integration can run flawlessly.

PROJECT_ID="garissadrm"

echo "⚙️ Setting active project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

echo "🚀 Enabling required APIs for Agent Builder / Garden Platform..."

# Enable Agent Platform & Registry
gcloud services enable agentregistry.googleapis.com
gcloud services enable agentplatform.googleapis.com

# Enable App Hub & Topology
gcloud services enable apphub.googleapis.com
gcloud services enable apptopology.googleapis.com

# Enable Cloud API Registry
gcloud services enable cloudapiregistry.googleapis.com

# Enable IAM (Identity and Access Management)
gcloud services enable iam.googleapis.com

# Enable IAM Connectors
gcloud services enable iamconnectors.googleapis.com

# Enable Cloud Identity-Aware Proxy
gcloud services enable iap.googleapis.com

# Enable Model Armor
gcloud services enable modelarmor.googleapis.com

# Enable Network Security & Services
gcloud services enable networksecurity.googleapis.com
gcloud services enable networkservices.googleapis.com

# Enable Notebooks API
gcloud services enable notebooks.googleapis.com

# Enable Observability API
gcloud services enable observability.googleapis.com

# Enable App Lifecycle Manager
gcloud services enable applifecyclemanager.googleapis.com

# Enable Security Command Center
gcloud services enable securitycenter.googleapis.com

# Enable Telemetry API
gcloud services enable telemetry.googleapis.com

# Extra check for Gemini/Vertex AI core services
gcloud services enable aiplatform.googleapis.com
gcloud services enable dialogflow.googleapis.com
gcloud services enable discoveryengine.googleapis.com

echo "✅ SUCCESS! All required Agent Platform APIs have been enabled."
echo "You can now refresh the Agent Garden page in the GCP Console."
