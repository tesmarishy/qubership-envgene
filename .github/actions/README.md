# Composite Actions

Этот каталог содержит composite actions для сборки Docker образов Qubership.

## Доступные Actions

### build-gcip
Сборка Docker образа для Qubership GCIP.

**Входные параметры:**
- `registry` (опционально): URL контейнерного реестра (по умолчанию: `ghcr.io`)
- `image-name` (опционально): Имя Docker образа (по умолчанию: `netcracker/qubership-gcip`)
- `dockerfile-path` (опционально): Путь к Dockerfile (по умолчанию: `./build_gcip/build/Dockerfile`)
- `git-user` (опционально): Git username для build args
- `git-token` (опционально): Git token для build args

### build-envgene
Сборка Docker образа для Qubership Envgene.

**Входные параметры:**
- `registry` (опционально): URL контейнерного реестра (по умолчанию: `ghcr.io`)
- `image-name` (опционально): Имя Docker образа (по умолчанию: `netcracker/qubership-envgene`)
- `dockerfile-path` (опционально): Путь к Dockerfile (по умолчанию: `./build_envgene/build/Dockerfile`)
- `gh-access-token` (опционально): GitHub access token для build args

### build-pipeline
Сборка Docker образа для Instance Repo Pipeline.

**Входные параметры:**
- `registry` (опционально): URL контейнерного реестра (по умолчанию: `ghcr.io`)
- `image-name` (опционально): Имя Docker образа (по умолчанию: `netcracker/qubership-instance-repo-pipeline`)
- `dockerfile-path` (опционально): Путь к Dockerfile (по умолчанию: `./github_workflows/instance-repo-pipeline/Dockerfile`)
- `gh-access-token` (опционально): GitHub access token для build args

### build-effective-set
Сборка Docker образа для Effective Set Generator с предварительной сборкой JAR.

**Входные параметры:**
- `registry` (опционально): URL контейнерного реестра (по умолчанию: `ghcr.io`)
- `image-name` (опционально): Имя Docker образа (по умолчанию: `netcracker/qubership-effective-set-generator`)
- `dockerfile-path` (опционально): Путь к Dockerfile (по умолчанию: `./build_effective_set_generator_java/Dockerfile`)
- `pom-path` (опционально): Путь к Maven POM файлу (по умолчанию: `./build_effective_set_generator_java/pom.xml`)
- `git-user` (опционально): Git username для build args
- `git-token` (опционально): Git token для build args

## Использование

### В workflow файле:
```yaml
- name: Build Docker Image
  uses: ./.github/actions/build-gcip
  with:
    registry: ghcr.io
    git-user: ${{ secrets.GIT_USER }}
    git-token: ${{ secrets.GIT_TOKEN }}
```

### Параллельная сборка всех образов:
Используйте workflow `build-all-docker-images.yml`, который запускает все четыре сборки параллельно после выполнения тестов. 