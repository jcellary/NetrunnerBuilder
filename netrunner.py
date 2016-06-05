# coding: utf-8

import xml.etree.ElementTree as ET
import operator
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class NetrunnerBuilder:

    card_definitions = {}

    set_root_dir = u"C:\\Users\\Jarosław\\Dysk Google\\Dokumenty\\OCTGN\\GameDatabase\\0f38e453-26df-4c04-9d67-6d43de939c77\\Sets\\"

    set_groups = [
        {'name': 'Core Set', 'ids': ['975fe9ee-7c7c-4d05-bd35-d159f92a1294']},
        {'name': 'Genesis Cycle', 'ids': [
            '906bdbcf-b1de-43a1-b17b-0b4ae7332506',
            '36787cac-674a-459c-b11c-ef23a5d78045',
            'ed18992f-8f53-4335-a7f2-44a96fbb8ee1',
            '457db4e2-86b4-4621-8149-4e72bf27db1d',
            '54e6b622-c596-4216-ba49-c728e6003525',
            '5b83cf2c-1faf-4a5d-816d-0fcaa77a40c2'
        ]},
        {'name': 'Creation and Control', 'ids': ['4be654e8-095a-4886-9817-53a78b9d6930']},
        {'name': 'The Spin Cycle', 'ids': [
            'b0378768-f775-4216-8a4d-40634294898c',
            '628d9e22-e803-4362-a22a-d59179d232bd',
            '08c831e8-8920-4fc0-b08e-f6dedbd2bcc4',
            '3655b61a-9514-41b2-858c-f271ed898556',
            '53f16ba2-4c63-4e7f-93e7-5d4635b58027',
            'fc30376d-ee87-4d89-a0aa-634181c9baca'
        ]},
        {'name': 'Honor and Profit', 'ids': ['acd4a6e4-c83e-43ea-b367-114d2fc9bf49']},
        {'name': 'The Lunar Cycle', 'ids': [
            'd5fe03a8-4e4d-4bc4-8117-4c2c6e2366e3',
            'a76c6360-dd0d-4742-9d31-99ae30341a32',
            '6d53e0c7-87c4-42f4-902f-ec61cb0d442c',
            '975dcca7-751b-40f6-9815-78d946f93c95',
            '9a2742b2-92ad-4e4b-9069-0b374aff795f',
            '006012c6-2fc1-49b3-835d-33c378a97b8c'
        ]},
        {'name': 'Order and Chaos', 'ids': ['7ef1d32e-bb98-44b5-a183-78f0d19d9e1c']},
        {'name': 'SanSan Cycle', 'ids': [
            '02195040-be86-448a-808d-90611d2b3b75',
            'c8b7128f-7233-48c0-bd4d-c3c5bf54b171',
            'b6a31aa5-faae-4fd3-8464-f910e70e9362',
            '16fc7570-471d-4a99-87bc-e5e1c28c6b2f',
            '5e65011b-2788-46ea-8d9f-27a0c23358ac',
            'daed7a4d-3de9-4b70-b50e-f6f4a6227ce4'
        ]},
        {'name': 'Data and Destiny', 'ids': ['29780fb4-5778-4619-9f28-3431c4857b1d']},
        {'name': 'Mumbad Cycle', 'ids': [
            'd44c7852-e2e1-4ac3-88f3-d791a4412994',
            '3ed05c61-2293-4307-b33e-5e5f3aec3a29',
        ]}
    ]

    def load_set(self, set_id, card_counter, cycle_name, subset_number):
        card_no = 0
        tree = ET.parse(self.set_root_dir + set_id + '\\set.xml')
        for card in tree.getroot().iter('card'):
            card_id = card.attrib.get('id')
            self.card_definitions[card_id] = dict(
                id=card_id,
                name=card.attrib.get('name'),
                faction=card.find('property[@name="Faction"]').attrib.get('value') or "Neutral",
                number=card_counter + card_no,
                set_id=set_id,
                subset_number=subset_number,
                cycle_name=cycle_name
            )
            card_no += 1
        return card_no

    def load_sets(self):
        subset_number = 0
        for group in self.set_groups:
            card_counter = 1
            for set_id in group['ids']:
                card_counter += self.load_set(set_id, card_counter, group['name'], subset_number)
                subset_number += 1

    @staticmethod
    def read_deck(deck_file):
        tree = ET.parse(deck_file)
        cards = []
        for card in list(tree.getroot().iter('section'))[1].iter('card'):
            cards.append(dict(
                quantity=card.attrib['qty'],
                id=card.attrib['id'],
                name=card.text
            ))
        return cards

    @staticmethod
    def value_or_default(dictionary, key, default):
        if dictionary is not None:
            return dictionary[key]
        else:
            return default

    def merge_card_def(self, cards):
        enriched_cards = []
        for card in cards:
            card_def = self.card_definitions.get(card['id'])
            enriched_cards.append(dict(
                name=card['name'],
                quantity=card['quantity'],
                id=self.value_or_default(card_def, 'id', card['name']),
                number=self.value_or_default(card_def, 'number', 0),
                faction=self.value_or_default(card_def, 'faction', '?'),
                subset_number=self.value_or_default(card_def, 'subset_number', 0),
                cycle_name=self.value_or_default(card_def, 'cycle_name', '?')
            ))
        return enriched_cards

    @staticmethod
    def get_deck_diff(current_cards, next_cards):
        intersected_cards = []
        for current_card in current_cards:
            next_card = next((card for card in next_cards if card['id'] == current_card['id']), None)
            if next_card is not None:
                intersected_cards.append([current_card, next_card])

        return intersected_cards

    @staticmethod
    def print_diff(intersected_cards):
        for card_pair in intersected_cards:
            print str.format('{0};{1};{2};{3};{4};{5}',
            #print str.format('{0:15} {1:5} {2:20} {3:5} {4:30}',
                             card_pair[0]['faction'],
                             card_pair[0]['quantity'],
                             card_pair[0]['cycle_name'],
                             card_pair[0]['number'],
                             card_pair[0]['name'],
                             card_pair[1]['quantity'])


    @staticmethod
    def print_cards(enriched_cards):
        for card in enriched_cards:
            print str.format('{0};{1};{2};{3};{4}',
            #print str.format('{0:15} {1:5} {2:20} {3:5} {4:30}',
                             card['faction'],
                             card['quantity'],
                             card['cycle_name'],
                             card['number'],
                             card['name'])

    def init(self):
        self.load_sets()

    def get_enriched_deck(self, deck_file):
        cards = self.read_deck(deck_file)
        enriched_cards = self.merge_card_def(cards)
        enriched_cards = sorted(enriched_cards, key=operator.itemgetter('faction', 'subset_number', 'number'))
        return enriched_cards

    def process_and_print_side(self, current_deck_path, next_deck_path, side_name):
        current_cards = self.get_enriched_deck(current_deck_path)
        print str.format('\nCurrent {0}:\n', side_name)
        self.print_cards(current_cards)

        next_cards = self.get_enriched_deck(next_deck_path)
        print str.format('\nNext {0}:\n', side_name)
        self.print_cards(next_cards)

        next_cards = self.get_deck_diff(current_cards, next_cards)
        print str.format('\nDiff {0}:\n', side_name)
        self.print_diff(next_cards)

    def run(self):
        self.init()

        path = 'C:\\Jar\\Programowanie\\Python\\NetrunnerBuilder\\'
        current_corp_path = path + 'current_corp.o8d'
        next_corp_path = path + 'next_corp.o8d'
        current_runner_path = path + 'current_runner.o8d'
        next_runner_path = path + 'next_runner.o8d'

        self.process_and_print_side(current_corp_path, next_corp_path, "Corp")
        self.process_and_print_side(current_runner_path, next_runner_path, "Runner")


builder = NetrunnerBuilder()
builder.run()