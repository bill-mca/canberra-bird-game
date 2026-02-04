#!/usr/bin/env python3
"""
Add structured rarity and status fields to bird entries
"""

import json
import re

def parse_rarity(status_text):
    """Extract rarity level from status text"""
    status_lower = status_text.lower()

    if 'very common' in status_lower:
        return 'very_common'
    elif 'common' in status_lower:
        return 'common'
    elif 'uncommon' in status_lower:
        return 'uncommon'
    elif 'rare' in status_lower:
        return 'rare'
    elif 'vagrant' in status_lower:
        return 'vagrant'
    elif 'extinct' in status_lower:
        return 'extinct'
    else:
        return 'unknown'


def parse_breeding_status(status_text):
    """Extract breeding/migration status from status text"""
    status_lower = status_text.lower()

    # Check for various patterns
    patterns = {
        'breeding_resident': r'breeding resident(?!/)',
        'breeding_visitor': r'breeding visitor',
        'breeding_summer_migrant': r'breeding summer (migrant|visitor)',
        'breeding_winter_migrant': r'breeding winter (migrant|visitor)',
        'breeding_autumn_migrant': r'breeding autumn migrant',
        'breeding_migrant': r'breeding migrant',
        'non_breeding_visitor': r'non-breeding (visitor|resident)',
        'non_breeding_summer_migrant': r'non-breeding summer migrant',
        'non_breeding_winter_migrant': r'non-breeding winter migrant',
        'non_breeding_autumn_migrant': r'non-breeding autumn migrant',
        'altitudinal_migrant': r'altitudinal migrant',
        'breeding_resident_or_migrant': r'breeding resident/(summer )?migrant',
        'breeding_resident_or_visitor': r'breeding resident/visitor',
    }

    for status_type, pattern in patterns.items():
        if re.search(pattern, status_lower):
            return status_type

    return None


def parse_conservation_status(status_text):
    """Extract conservation status from status text"""
    status_lower = status_text.lower()

    # Check for conservation status in order of severity
    if 'critically endangered' in status_lower:
        # Extract which jurisdiction(s)
        jurisdictions = []
        if 'critically endangered epbc' in status_lower:
            jurisdictions.append('EPBC')
        if 'critically endangered nsw' in status_lower:
            jurisdictions.append('NSW')
        if 'critically endangered act' in status_lower:
            jurisdictions.append('ACT')
        return {
            'level': 'critically_endangered',
            'jurisdictions': jurisdictions if jurisdictions else ['unknown']
        }
    elif 'endangered' in status_lower:
        jurisdictions = []
        if 'endangered epbc' in status_lower:
            jurisdictions.append('EPBC')
        if 'endangered nsw' in status_lower:
            jurisdictions.append('NSW')
        if 'endangered act' in status_lower:
            jurisdictions.append('ACT')
        return {
            'level': 'endangered',
            'jurisdictions': jurisdictions if jurisdictions else ['unknown']
        }
    elif 'vulnerable' in status_lower:
        jurisdictions = []
        if 'vulnerable epbc' in status_lower:
            jurisdictions.append('EPBC')
        if 'vulnerable nsw' in status_lower:
            jurisdictions.append('NSW')
        if 'vulnerable act' in status_lower:
            jurisdictions.append('ACT')
        return {
            'level': 'vulnerable',
            'jurisdictions': jurisdictions if jurisdictions else ['unknown']
        }

    return None


def parse_origin_status(status_text):
    """Extract origin information (introduced, reintroduced, escapee)"""
    status_lower = status_text.lower()

    result = {
        'isIntroduced': 'introduced' in status_lower,
        'isReintroduced': 'reintroduced' in status_lower,
        'isEscapee': 'escapee' in status_lower
    }

    return result


def add_structured_fields():
    """Add structured fields to all bird entries"""

    # Load the bird data
    with open('data/act_birds.json', 'r') as f:
        data = json.load(f)

    birds = data['birds']

    print(f"Processing {len(birds)} bird species...")
    print()

    # Statistics
    rarity_counts = {}
    conservation_counts = {}
    introduced_count = 0

    for i, bird in enumerate(birds):
        status_text = bird.get('statusInACT', '')

        # Parse and add structured fields
        bird['rarity'] = parse_rarity(status_text)
        bird['breedingStatus'] = parse_breeding_status(status_text)
        bird['conservationStatus'] = parse_conservation_status(status_text)

        origin = parse_origin_status(status_text)
        bird['isIntroduced'] = origin['isIntroduced']
        bird['isReintroduced'] = origin['isReintroduced']
        bird['isEscapee'] = origin['isEscapee']

        # Update statistics
        rarity = bird['rarity']
        rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1

        if bird['conservationStatus']:
            level = bird['conservationStatus']['level']
            conservation_counts[level] = conservation_counts.get(level, 0) + 1

        if bird['isIntroduced']:
            introduced_count += 1

        # Show progress for some interesting ones
        if bird.get('conservationStatus') and bird['conservationStatus']['level'] in ['critically_endangered', 'endangered']:
            print(f"  {bird['commonName']}: {bird['conservationStatus']['level'].replace('_', ' ').title()} "
                  f"({', '.join(bird['conservationStatus']['jurisdictions'])})")

    # Update statistics
    data['statistics']['rarityDistribution'] = rarity_counts
    data['statistics']['conservationStatusCounts'] = conservation_counts
    data['statistics']['introducedSpecies'] = introduced_count

    # Save updated JSON
    with open('data/act_birds.json', 'w') as f:
        json.dump(data, f, indent=2)

    print()
    print("=== Summary ===")
    print(f"\nRarity Distribution:")
    for rarity, count in sorted(rarity_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rarity.replace('_', ' ').title()}: {count} species")

    print(f"\nConservation Status:")
    if conservation_counts:
        for status, count in sorted(conservation_counts.items()):
            print(f"  {status.replace('_', ' ').title()}: {count} species")
    else:
        print("  No species with conservation concerns")

    print(f"\nOrigin:")
    print(f"  Introduced species: {introduced_count}")
    print(f"  Native species: {len(birds) - introduced_count}")

    print(f"\nUpdated data/act_birds.json successfully!")


if __name__ == '__main__':
    add_structured_fields()
