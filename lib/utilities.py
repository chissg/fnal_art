from pathlib import Path


def preset_args(source_path):
    if (Path(source_path) / "CMakePresets.json").exists():
        return ["--preset", "default"]
    return []


def sanitize_environments(env, *env_vars):
    for var in env_vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)
