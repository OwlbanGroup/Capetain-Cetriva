"""Demo script for generating account numbers and resolving routing numbers.

Uses BankingUtils to produce a valid account number for the project bank,
retrieve its routing number, and validate that routing number.
"""
from banking_utils import BankingUtils


def main():
    """Run the account/routing demo and print the results."""
    bank_utils = BankingUtils()

    # Generate a valid account number
    account_number = bank_utils.generate_account(10)
    print(f"Generated Account Number: {account_number}")

    # Retrieve routing number for the project bank
    bank_name = "Capetain Cetriva"
    routing_number = bank_utils.get_routing(bank_name)
    print(f"Routing Number for {bank_name}: {routing_number}")

    # Validate the retrieved routing number
    if routing_number:
        is_valid = bank_utils.validate_routing(routing_number)
        print(f"Is Routing Number Valid? {is_valid}")
    else:
        print("Failed to retrieve routing number.")


if __name__ == "__main__":
    main()flowchart TD
    subgraph Cluster["OpenShift Cluster (RHEL CoreOS)"]
        direction TB

        subgraph Virt["OpenShift Virtualization (KubeVirt)"]
            VM1["Legacy VM App"]
            VM2["Compliance VM"]
        end

        subgraph Containers["Blackbox AI Container Layer"]
            BBAPI["Blackbox Core API"]
            EXTAPI["Extensions API"]
            PAY["Payroll Engine"]
            FRAUD["Fraud Detection"]
            CALLBACK["Callback Handler Engine"]
        end

        subgraph GPU["GPU AI Layer"]
            TRITON["Triton Inference Server"]
            ERA["Blackbox AI Era Engines"]
        end

        NET["OpenShift Networking (Service/Route/Ingress)"]
        GITOPS["ArgoCD GitOps Pipeline"]
        PIPE["Tekton CI/CD"]
    end

    VM1 --> NET
    VM2 --> NET
    BBAPI --> NET
    EXTAPI --> NET
    PAY --> NET
    FRAUD --> NET
    CALLBACK --> NET

    NET --> TRITON
    NET --> ERA

    GITOPS --> Virt
    GITOPS --> Containers
    GITOPS --> GPU
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: legacy-financial-app
spec:
  running: true
  template:
    spec:
      domain:
        cpu:
          cores: 2
        devices:
          disks:
            - name: rootdisk
              disk:
                bus: virtio
      volumes:
        - name: rootdisk
          containerDisk:
            image: quay.io/blackbox/legacy-financial-app-vm:latest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: financial-app-modern
spec:
  replicas: 2
  selector:
    matchLabels:
      app: financial-app-modern
  template:
    metadata:
      labels:
        app: financial-app-modern
    spec:
      containers:
        - name: app
          image: quay.io/blackbox/financial-app-container:latest
# Switch target by changing this label
appMode: vm   # or "container"
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: blackbox-modernization
spec:
  project: default
  source:
    repoURL: https://github.com/OwlbanGroup/blackbox-gitops
    path: apps
  destination:
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
