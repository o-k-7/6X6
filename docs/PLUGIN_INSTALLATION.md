# Install the 6X6 plugin

6X6 is packaged as a skills-only plugin. It requests no account, network connection, provider credential, or paid service.

## ChatGPT and Codex

The public ChatGPT and Codex Plugins Directory requires review by OpenAI. Until the public listing is approved, a workspace administrator can import this GitHub repository as a marketplace source, or a developer can install the local package from `plugins/6x6/`.

The submitted package is `plugins/6x6/`. It contains the portable manifest, the Codex manifest, the skill, its specification, and local image assets.

Installing the plugin makes 6X6 available to the host. It does not make 6X6 an always-on default and cannot override higher-priority host or safety instructions.

## Claude Code

Add the GitHub marketplace and install 6X6:

```text
/plugin marketplace add o-k-7/6X6
/plugin install 6x6@ok7-plugins
```

Equivalent terminal commands:

```bash
claude plugin marketplace add o-k-7/6X6
claude plugin install 6x6@ok7-plugins
```

The public `claude-community` listing requires review by Anthropic. The repository marketplace works independently of that listing.

## Verify the package

```bash
python -m unittest tests.test_plugin_package -v
python /path/to/plugin-creator/scripts/validate_plugin.py plugins/6x6
claude plugin validate .
```

The Claude command requires Claude Code. The other checks require only Python 3.10 or newer.
