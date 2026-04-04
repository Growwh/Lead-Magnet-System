# Contributing to Lead Magnet System In A Box

Thanks for your interest in contributing. Here's how to get started.

## How to Contribute

1. **Fork** the repo
2. **Clone** your fork locally
3. **Create a branch** for your feature or fix (`git checkout -b feature/your-feature`)
4. **Make your changes** and test them
5. **Commit** with a clear message describing the change
6. **Push** to your fork and open a **Pull Request**

## What to Contribute

- Bug fixes
- New content fetcher platforms (e.g. X/Twitter, Instagram)
- New output format scripts
- Improvements to existing scripts
- Documentation improvements

## Code Style

- Python 3.11+
- No type: ignore comments without explanation
- Scripts should work standalone via CLI (`python scripts/script.py --help`)
- All external URLs must go through SSRF protection (`_is_private_url`)

## Reporting Issues

Open an issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your Python version and OS

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
