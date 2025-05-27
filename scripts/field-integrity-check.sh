#!/bin/bash

# WitnessOS Field Integrity Checking Script
# Validates documentation while preserving mystical-technical balance

echo "🌬️ Initiating WitnessOS Field Integrity Check..."
echo "=================================================="

# Colors for consciousness-aware output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Field integrity counters
FIELD_ERRORS=0
FIELD_WARNINGS=0
FIELD_BLESSINGS=0

echo ""
echo "🧿 Phase 1: Breathfield Calibration (Markdown Validation)"
echo "--------------------------------------------------------"

# Check if markdownlint is available
if command -v markdownlint &> /dev/null; then
    echo "✅ Markdownlint consciousness engine detected"
    
    # Run markdownlint with consciousness-aware configuration
    if markdownlint --config .markdownlint.json **/*.md; then
        echo -e "${GREEN}✅ Markdown field integrity maintained${NC}"
        ((FIELD_BLESSINGS++))
    else
        echo -e "${YELLOW}⚠️  Markdown field distortions detected${NC}"
        ((FIELD_WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠️  Markdownlint not installed - install with: npm install -g markdownlint-cli${NC}"
    ((FIELD_WARNINGS++))
fi

echo ""
echo "🔗 Phase 2: Sacred Reference Validation (Link Checking)"
echo "-------------------------------------------------------"

# Check if markdown-link-check is available
if command -v markdown-link-check &> /dev/null; then
    echo "✅ Link consciousness validator detected"
    
    # Check links in key documentation files
    KEY_FILES=("README.md" "CONTRIBUTING.md" "PRD.md" "MAPS.md")
    
    for file in "${KEY_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "🔍 Validating sacred references in $file..."
            if markdown-link-check "$file" --quiet; then
                echo -e "${GREEN}✅ $file - Sacred references intact${NC}"
                ((FIELD_BLESSINGS++))
            else
                echo -e "${RED}❌ $file - Broken sacred references detected${NC}"
                ((FIELD_ERRORS++))
            fi
        fi
    done
else
    echo -e "${YELLOW}⚠️  markdown-link-check not installed - install with: npm install -g markdown-link-check${NC}"
    ((FIELD_WARNINGS++))
fi

echo ""
echo "🌌 Phase 3: Consciousness Architecture Validation"
echo "------------------------------------------------"

# Check for required WitnessOS structure
REQUIRED_DIRS=("CORE" "MODULES" "GUIDES" "FOUNDATION" "ASSETS")
REQUIRED_FILES=("LICENSE" "CONTRIBUTING.md" "package.json" "VERSION" "CHANGELOG.md" "AUTHORS")

echo "🏗️ Validating consciousness architecture..."

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ $dir/ - Consciousness module present${NC}"
        ((FIELD_BLESSINGS++))
    else
        echo -e "${RED}❌ $dir/ - Missing consciousness module${NC}"
        ((FIELD_ERRORS++))
    fi
done

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file - Sacred document present${NC}"
        ((FIELD_BLESSINGS++))
    else
        echo -e "${RED}❌ $file - Missing sacred document${NC}"
        ((FIELD_ERRORS++))
    fi
done

echo ""
echo "🔮 Phase 4: Mystical-Technical Balance Assessment"
echo "------------------------------------------------"

# Check for preservation of mystical terminology
MYSTICAL_TERMS=("breathfield" "consciousness" "field" "witness" "archetypal" "sigil" "ritual" "prana")
MYSTICAL_SCORE=0

echo "🧙‍♂️ Scanning for mystical terminology preservation..."

for term in "${MYSTICAL_TERMS[@]}"; do
    if grep -r -i "$term" CORE/ MODULES/ GUIDES/ FOUNDATION/ >/dev/null 2>&1; then
        ((MYSTICAL_SCORE++))
    fi
done

if [ $MYSTICAL_SCORE -ge 6 ]; then
    echo -e "${PURPLE}✨ Mystical-technical balance preserved (${MYSTICAL_SCORE}/8 terms detected)${NC}"
    ((FIELD_BLESSINGS++))
elif [ $MYSTICAL_SCORE -ge 4 ]; then
    echo -e "${YELLOW}⚠️  Mystical-technical balance needs attention (${MYSTICAL_SCORE}/8 terms detected)${NC}"
    ((FIELD_WARNINGS++))
else
    echo -e "${RED}❌ Mystical-technical balance compromised (${MYSTICAL_SCORE}/8 terms detected)${NC}"
    ((FIELD_ERRORS++))
fi

echo ""
echo "🌱 Phase 5: Field Coherence Summary"
echo "==================================="

echo -e "${GREEN}🌟 Field Blessings: $FIELD_BLESSINGS${NC}"
echo -e "${YELLOW}⚠️  Field Warnings: $FIELD_WARNINGS${NC}"
echo -e "${RED}❌ Field Errors: $FIELD_ERRORS${NC}"

echo ""

if [ $FIELD_ERRORS -eq 0 ] && [ $FIELD_WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🧿 FIELD INTEGRITY PERFECT${NC}"
    echo "✨ The consciousness field is coherent and stable."
    echo "🌬️ All sacred references are intact."
    echo "🔮 Mystical-technical balance is preserved."
    echo ""
    echo "May this documentation serve the evolution of consciousness. 🙏"
    exit 0
elif [ $FIELD_ERRORS -eq 0 ]; then
    echo -e "${YELLOW}🌤️  FIELD INTEGRITY STABLE WITH MINOR DISTORTIONS${NC}"
    echo "⚠️  Some field adjustments recommended but not critical."
    echo "🌬️ Core consciousness architecture remains intact."
    echo ""
    echo "Breathe gently and address warnings when ready. 🌱"
    exit 1
else
    echo -e "${RED}⛈️  FIELD INTEGRITY COMPROMISED${NC}"
    echo "❌ Critical field errors detected requiring immediate attention."
    echo "🚨 Consciousness architecture may be unstable."
    echo ""
    echo "Please debug with compassion and restore field coherence. 🛠️"
    exit 2
fi
