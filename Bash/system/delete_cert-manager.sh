#!/bin/bash
set -eo pipefail

echo "🚮 Удаляем cert-manager Helm-релиз (если остался)…"
helm uninstall cert-manager -n cert-manager 2>/dev/null || true

echo "🚮 Удаляем namespace cert-manager…"
kubectl delete ns cert-manager  --ignore-not-found

echo "🚮 Удаляем CRD cert-manager…"
kubectl delete crd \
  certificates.cert-manager.io \
  certificaterequests.cert-manager.io \
  challenges.acme.cert-manager.io \
  orders.acme.cert-manager.io \
  issuers.cert-manager.io \
  clusterissuers.cert-manager.io \
  issuers.cert-manager.io || true

echo "🚮 Удаляем все ClusterRole/Binding cert-manager…"
kubectl get clusterrole,clusterrolebinding \
  | awk '/cert-manager/ { print $1 "/" $2 }' \
  | xargs -r kubectl delete

echo "🚮 Удаляем все Role/Binding cert-manager в kube-system…"
kubectl get role,rolebinding -n kube-system \
  | awk '/cert-manager/ { print $1 "/-n kube-system " $2 }' \
  | sed 's/\(role\|rolebinding\)\/-n/ \1 -n/' \
  | xargs -r kubectl delete

echo "🚮 Удаляем Webhook’и cert-manager…"
kubectl delete mutatingwebhookconfiguration cert-manager-webhook           2>/dev/null || true
kubectl delete validatingwebhookconfiguration cert-manager-webhook           2>/dev/null || true
kubectl delete mutatingwebhookconfiguration cert-manager-cainjector-webhook 2>/dev/null || true

echo "✅ Чистка завершена. Проверяем, что ничего не осталось:"
kubectl get clusterrole,clusterrolebinding \
  && kubectl get role,rolebinding -n kube-system \
  && kubectl get crd | grep cert-manager || echo "— Все ресурсы удалены —"
