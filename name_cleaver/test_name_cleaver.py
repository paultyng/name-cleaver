from name_cleaver import PoliticianNameCleaver, OrganizationNameCleaver, \
        IndividualNameCleaver

import unittest


class TestPoliticianNameCleaver(unittest.TestCase):

    def test_case_converts_in_non_mixed_case_names_only(self):
        self.assertEqual('Antonio dAlesio', str(PoliticianNameCleaver('Antonio dAlesio').parse()))

    def test_upper_case_scot_with_party(self):
        self.assertEqual('Emory MacDonald', str(PoliticianNameCleaver('MACDONALD, EMORY (R)').parse()))

    def test_last_first_mixed_case_scot_with_party(self):
        self.assertEqual('Emory MacDonald', str(PoliticianNameCleaver('MacDonald, Emory (R)').parse()))

    def test_first_last_mixed_case_with_party(self):
        self.assertEqual('Nancy Pelosi', str(PoliticianNameCleaver('Nancy Pelosi (D)').parse()))

    def test_not_everything_is_a_scot(self):
        self.assertEqual('Adam Mack', str(PoliticianNameCleaver('ADAM MACK').parse()))
        self.assertEqual('Don Womackey', str(PoliticianNameCleaver('DON WOMACKEY').parse()))

    def test_last_first(self):
        self.assertEqual('Albert Gore', str(PoliticianNameCleaver('Gore, Albert').parse()))

    def test_pile_it_on(self):
        self.assertEqual('Milton Elmer McCullough Jr', str(PoliticianNameCleaver('Milton Elmer "Mac" McCullough, Jr (3)').parse()))

    def test_pile_it_on_two(self):
        self.assertEqual('William Steve Southerland II', str(PoliticianNameCleaver('William Steve Southerland  II (R)').parse()))

    def test_pile_it_on_three(self):
        self.assertEqual('Edward Thomas O\'Donnell Jr', str(PoliticianNameCleaver('Edward Thomas O\'Donnell, Jr (D)').parse()))

    def test_standardize_running_mate_names(self):
        self.assertEqual('John Kasich & Mary Taylor', str(PoliticianNameCleaver('Kasich, John & Taylor, Mary').parse()))

    def test_we_dont_need_no_steeenking_nicknames(self):
        self.assertEqual('Robert M McDonnell', str(PoliticianNameCleaver('McDonnell, Robert M (Bob)').parse()))
        self.assertEqual('John J Duncan Jr', str(PoliticianNameCleaver('John J (Jimmy) Duncan Jr (R)').parse()))
        self.assertEqual('Christopher Bond', str(PoliticianNameCleaver('Christopher "Kit" Bond').parse()))

    def test_capitalize_roman_numeral_suffixes(self):
        self.assertEqual('Ken Cuccinelli II', str(PoliticianNameCleaver('KEN CUCCINELLI II').parse()))
        self.assertEqual('Ken Cuccinelli II', str(PoliticianNameCleaver('CUCCINELLI II, KEN').parse()))
        self.assertEqual('Ken Cuccinelli IV', str(PoliticianNameCleaver('CUCCINELLI IV, KEN').parse()))
        self.assertEqual('Ken Cuccinelli IX', str(PoliticianNameCleaver('CUCCINELLI IX, KEN').parse()))

    def test_name_with_two_part_last_name(self):
        self.assertEqual('La Mere', PoliticianNameCleaver('Albert J La Mere').parse().last)
        self.assertEqual('Di Souza', PoliticianNameCleaver('Dinesh Di Souza').parse().last)

    def test_deals_with_last_names_that_look_like_two_part_but_are_not(self):
        name = PoliticianNameCleaver('Quoc Van (D)').parse()
        self.assertEqual('Quoc', name.first)
        self.assertEqual('Van', name.last)

    def test_doesnt_misinterpret_roman_numeral_characters_in_last_name_as_suffix(self):
        self.assertEqual('Vickers', PoliticianNameCleaver('Audrey C Vickers').parse().last)

    def test_multiple_middle_names(self):
        self.assertEqual('Swift Eagle', PoliticianNameCleaver('Alexander Swift Eagle Justice').parse().middle)

    def test_edgar_de_lisle_ross(self):
        name = PoliticianNameCleaver('Edgar de L\'Isle Ross (R)').parse()
        self.assertEqual('Edgar', name.first)
        self.assertEqual('de L\'Isle', name.middle)
        self.assertEqual('Ross', name.last)
        self.assertEqual(None, name.suffix)

    def test_with_metadata(self):
        self.assertEqual('Charles Schumer (D-NY)', str(PoliticianNameCleaver('Charles Schumer').parse().plus_metadata('D', 'NY')))
        self.assertEqual('Barack Obama (D)', str(PoliticianNameCleaver('Barack Obama').parse().plus_metadata('D', '')))
        self.assertEqual('Charles Schumer (NY)', str(PoliticianNameCleaver('Charles Schumer').parse().plus_metadata('', 'NY')))
        self.assertEqual('Jerry Leon Carroll', str(PoliticianNameCleaver('Jerry Leon Carroll').parse().plus_metadata('', ''))) # only this one guy is missing both at the moment

    def test_running_mates_with_metadata(self):
        self.assertEqual('Ted Strickland & Lee Fischer (D-OH)', str(PoliticianNameCleaver('STRICKLAND, TED & FISCHER, LEE').parse().plus_metadata('D', 'OH')))

    def test_names_with_weird_parenthetical_stuff(self):
        self.assertEqual('Lynn Swann', str(PoliticianNameCleaver('SWANN, LYNN (COMMITTEE 1)').parse()))

    def test_handles_empty_names(self):
        self.assertEqual('', str(PoliticianNameCleaver('').parse()))

    def test_capitalize_irish_names(self):
        self.assertEqual('Sean O\'Leary', str(PoliticianNameCleaver('SEAN O\'LEARY').parse()))


class TestOrganizationNameCleaver(unittest.TestCase):

    def test_capitalize_pac(self):
        self.assertEqual('Nancy Pelosi Leadership PAC', str(OrganizationNameCleaver('NANCY PELOSI LEADERSHIP PAC').parse()))

    def test_make_single_word_names_ending_in_pac_all_uppercase(self):
        self.assertEqual('ECEPAC', str(OrganizationNameCleaver('ECEPAC').parse()))

    def test_names_starting_with_PAC(self):
        self.assertEqual('PAC For Engineers', str(OrganizationNameCleaver('PAC FOR ENGINEERS').parse()))
        self.assertEqual('PAC 102', str(OrganizationNameCleaver('PAC 102').parse()))

    def test_doesnt_bother_names_containing_string_pac(self):
        self.assertEqual('Pacific Trust', str(OrganizationNameCleaver('PACIFIC TRUST').parse()))

    def test_capitalize_scottish_names(self):
        self.assertEqual('McDonnell Douglas', str(OrganizationNameCleaver('MCDONNELL DOUGLAS').parse()))
        self.assertEqual('MacDonnell Douglas', str(OrganizationNameCleaver('MACDONNELL DOUGLAS').parse()))

    def test_dont_capitalize_just_anything_starting_with_mac(self):
        self.assertEqual('Machinists/Aerospace Workers Union', str(OrganizationNameCleaver('MACHINISTS/AEROSPACE WORKERS UNION').parse()))

    def test_expand(self):
        self.assertEqual('Raytheon Corporation', OrganizationNameCleaver('Raytheon Corp.').parse().expand())
        self.assertEqual('Massachusetts Institute of Technology', OrganizationNameCleaver('Massachusetts Inst. of Technology').parse().expand())

    def test_expand_with_two_tokens_to_expand(self):
        self.assertEqual('Merck & Company Incorporated', OrganizationNameCleaver('Merck & Co., Inc.').parse().expand())

    def test_dont_strip_after_hyphens_too_soon_in_a_name(self):
        self.assertEqual('US-Russia Business Council', OrganizationNameCleaver('US-Russia Business Council').parse().kernel())
        self.assertEqual('Wal-Mart Stores', OrganizationNameCleaver('Wal-Mart Stores, Inc.').parse().kernel())

    def test_strip_hyphens_more_than_three_characters_into_a_name(self):
        # This is not ideal for this name, but we can't get the best for all cases
        self.assertEqual('F Hoffmann', OrganizationNameCleaver('F. HOFFMANN-LA ROCHE LTD and its Affiliates').parse().kernel())

    def test_kernel(self):
        """
        Intended to get only the unique/meaningful words out of a name
        """
        self.assertEqual('Massachusetts Technology', OrganizationNameCleaver('Massachusetts Inst. of Technology').parse().kernel())
        self.assertEqual('Massachusetts Technology', OrganizationNameCleaver('Massachusetts Institute of Technology').parse().kernel())

        self.assertEqual('Walsh', OrganizationNameCleaver('The Walsh Group').parse().kernel())

        self.assertEqual('Health Net', OrganizationNameCleaver('Health Net Inc').parse().kernel())
        self.assertEqual('Health Net', OrganizationNameCleaver('Health Net, Inc.').parse().kernel())

        self.assertEqual('Distilled Spirits Council', OrganizationNameCleaver('Distilled Spirits Council of the U.S., Inc.').parse().kernel())

    def test_handles_empty_names(self):
        self.assertEqual('', str(OrganizationNameCleaver('').parse()))



class TestIndividualNameCleaver(unittest.TestCase):

    def test_all_kinds_of_crazy(self):
        self.assertEqual('Stanford Z Rothschild', str(IndividualNameCleaver('ROTHSCHILD 212, STANFORD Z MR').parse()))

    def test_jr_and_the_like_end_up_at_the_end(self):
        self.assertEqual('Frederick A "Tripp" Baird III', str(IndividualNameCleaver('Baird, Frederick A "Tripp" III').parse()))

    def test_nicknames_suffixes_and_honorifics(self):
        self.assertEqual('Frederick A "Tripp" Baird III', str(IndividualNameCleaver('Baird, Frederick A "Tripp" III Mr').parse()))
        self.assertEqual('Frederick A "Tripp" Baird III', str(IndividualNameCleaver('Baird, Mr Frederick A "Tripp" III').parse()))

    def test_throw_out_mr(self):
        self.assertEqual('T Boone Pickens', str(IndividualNameCleaver('Mr T Boone Pickens').parse()))
        self.assertEqual('T Boone Pickens', str(IndividualNameCleaver('Mr. T Boone Pickens').parse()))
        self.assertEqual('T Boone Pickens', str(IndividualNameCleaver('Pickens, T Boone Mr').parse()))
        self.assertEqual('John L Nau', str(IndividualNameCleaver(' MR JOHN L NAU,').parse()))

    def test_keep_the_mrs(self):
        self.assertEqual('Mrs. T Boone Pickens', str(IndividualNameCleaver('Mrs T Boone Pickens').parse()))
        self.assertEqual('Mrs. T Boone Pickens', str(IndividualNameCleaver('Mrs. T Boone Pickens').parse()))
        self.assertEqual('Mrs. Stanford Z Rothschild', str(IndividualNameCleaver('ROTHSCHILD 212, STANFORD Z MRS').parse()))

    def test_mrs_walton(self):
        self.assertEqual('Mrs. Jim Walton', str(IndividualNameCleaver('WALTON, JIM MRS').parse()))

    def test_capitalize_roman_numeral_suffixes(self):
        self.assertEqual('Ken Cuccinelli II', str(IndividualNameCleaver('KEN CUCCINELLI II').parse()))
        self.assertEqual('Ken Cuccinelli II', str(IndividualNameCleaver('CUCCINELLI II, KEN').parse()))
        self.assertEqual('Ken Cuccinelli IV', str(IndividualNameCleaver('CUCCINELLI IV, KEN').parse()))
        self.assertEqual('Ken Cuccinelli IX', str(IndividualNameCleaver('CUCCINELLI IX, KEN').parse()))

    def test_capitalize_scottish_last_names(self):
        self.assertEqual('Ronald McDonald', str(IndividualNameCleaver('RONALD MCDONALD').parse()))
        self.assertEqual('Old MacDonald', str(IndividualNameCleaver('OLD MACDONALD').parse()))

    def test_capitalizes_and_punctuates_initials(self):
        self.assertEqual('B.L. Schwartz', str(IndividualNameCleaver('SCHWARTZ, BL').parse()))

    def test_capitalizes_initials_but_not_honorifics(self):
        self.assertEqual('John Koza', str(IndividualNameCleaver('KOZA, DR JOHN').parse()))


class TestCapitalization(unittest.TestCase):

    def test_overrides_dumb_python_titlecasing_for_apostrophes(self):
        self.assertEqual('Phoenix Women\'s Health Center', str(OrganizationNameCleaver('PHOENIX WOMEN\'S HEALTH CENTER').parse()))


class TestOrganizationNameCleaverForIndustries(unittest.TestCase):

    def test_capitalizes_letter_after_slash(self):
        self.assertEqual('Health Services/Hmos', str(OrganizationNameCleaver('HEALTH SERVICES/HMOS').parse()))
        self.assertEqual('Lawyers/Law Firms', str(OrganizationNameCleaver('LAWYERS/LAW FIRMS').parse()))

    def test_capitalizes_letter_after_hyphen(self):
        self.assertEqual('Non-Profit Institutions', str(OrganizationNameCleaver('NON-PROFIT INSTITUTIONS').parse()))
        self.assertEqual('Pro-Israel', str(OrganizationNameCleaver('PRO-ISRAEL').parse()))

