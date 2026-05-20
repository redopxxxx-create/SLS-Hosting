from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RepoPlatform(StrEnum):
    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"
    HEROKU = "heroku"
    RENDER = "render"
    RAILWAY = "railway"
    KOYEB = "koyeb"
    VERCEL = "vercel"
    NETLIFY = "netlify"
    REPLIT = "replit"
    CODESANDBOX = "codesandbox"
    PYTHONANYWHERE = "pythonanywhere"
    VPS = "vps"
    DOCKER = "docker"
    GENERIC_GIT = "git"


@dataclass(slots=True)
class RepoInput:
    url: str
    token: str | None = None
    branch: str = "main"


def detect_platform(url: str) -> RepoPlatform:
    src = url.lower()
    if "github.com" in src:
        return RepoPlatform.GITHUB
    if "gitlab.com" in src:
        return RepoPlatform.GITLAB
    if "bitbucket.org" in src:
        return RepoPlatform.BITBUCKET
    if "heroku" in src:
        return RepoPlatform.HEROKU
    if "render.com" in src:
        return RepoPlatform.RENDER
    if "railway" in src:
        return RepoPlatform.RAILWAY
    if "koyeb" in src:
        return RepoPlatform.KOYEB
    if "vercel" in src:
        return RepoPlatform.VERCEL
    if "netlify" in src:
        return RepoPlatform.NETLIFY
    if "replit" in src:
        return RepoPlatform.REPLIT
    if "codesandbox" in src:
        return RepoPlatform.CODESANDBOX
    if "pythonanywhere" in src:
        return RepoPlatform.PYTHONANYWHERE
    return RepoPlatform.GENERIC_GIT
