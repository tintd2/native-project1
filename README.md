# native-project1
username: ${{ secrets.DOCKERHUB_USERNAME }}
password: ${{ secrets.DOCKERHUB_TOKEN }}

curl -sfL https://get.k3s.io | sh -
sudo su -
kubectl get no

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

admin/DKtpJlYwb4cxD2bK