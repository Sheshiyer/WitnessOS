# CONFIGURATION.md — WitnessOS Configuration Guide

This file provides instructions on how to configure the ENGINES and AVATARS within WitnessOS.

## 1. Engines Configuration

The ENGINES directory contains configuration files for various divination engines, such as Tarot, Gene Keys, and Enneagram.

### 1.1 Tarot Engine

The Tarot engine uses the `tarot.json` configuration file.

**Example:**

\`\`\`json
{
  "deck": "rider-waite",
  "spread": "three-card",
  "reversed": true
}
\`\`\`

**Parameters:**

*   `deck`: The Tarot deck to use (e.g., "rider-waite", "thoth").
*   `spread`: The spread to use (e.g., "three-card", "celtic-cross").
*   `reversed`: Whether to include reversed cards (true/false).

### 1.2 Gene Keys Engine

The Gene Keys engine uses the `gene-keys.json` configuration file.

**Example:**

\`\`\`json
{
  "profile": "activation-sequence",
  "center": "heart",
  "shadow": true
}
\`\`\`

**Parameters:**

*   `profile`: The Gene Keys profile to use (e.g., "activation-sequence", "venus-sequence").
*   `center`: The center to focus on (e.g., "heart", "ajna").
*   `shadow`: Whether to include shadow aspects (true/false).

### 1.3 Enneagram Engine

The Enneagram engine uses the `enneagram.json` configuration file.

**Example:**

\`\`\`json
{
  "type": "core",
  "wings": true,
  "integration": true
}
\`\`\`

**Parameters:**

*   `type`: The Enneagram type to focus on (e.g., "core", "wings").
*   `wings`: Whether to include wings (true/false).
*   `integration`: Whether to include integration/disintegration paths (true/false).

## 2. Avatars Configuration

The AVATARS directory contains data files for various avatars.

### 2.1 Avatar Data Files

Avatar data files are stored in JSON format.

**Example:**

\`\`\`json
{
  "name": "Aletheos",
  "archetype": "Runtime Architect",
  "description": "A skilled architect of consciousness runtimes.",
  "attributes": {
    "intelligence": 10,
    "wisdom": 9,
    "compassion": 8
  }
}
\`\`\`

**Parameters:**

*   `name`: The name of the avatar.
*   `archetype`: The archetype of the avatar.
*   `description`: A description of the avatar.
*   `attributes`: A set of attributes for the avatar.
