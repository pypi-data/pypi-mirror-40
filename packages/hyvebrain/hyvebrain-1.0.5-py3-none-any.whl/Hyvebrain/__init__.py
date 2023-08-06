name = "hyvebrain"
import requests, json

class Hyvebrain:

    URL_ENDPOINT = "https://api.hyvebrain.com/v/testing/"

    def __init__( self ):
        self.text_content = ""
        self.functions = []
        self._return_natural_language_raw_data = 0
        self._natural_language_raw_data = None

    def get_current_token_index( self ):
        self.functions.insert( 0, "get_current_token_index" )
        return self
    def get_current_sentence_index( self ):
        self.functions.insert( 0, "get_current_sentence_index" )
        return self

    def get_pos_tag( self ):
        self.functions.insert( 0, "get_pos_tag" )
        return self
    def get_depe_hti( self ):
        self.functions.insert( 0, "get_depe_hti" )
        return self
    def get_depe_label( self ):
        self.functions.insert( 0, "get_depe_label" )
        return self
    def get_pos_tag_str( self ):
        self.functions.insert( 0, "get_pos_tag_str" )
        return self
    def get_depe_label_str( self ):
        self.functions.insert( 0, "get_depe_label_str" )
        return self
    def get_lemma( self ):
        self.functions.insert( 0, "get_lemma" )
        return self
    def get_text_content_token( self ):
        self.functions.insert( 0, "get_text_content_token" )
        return self

    def get_token_index_list( self ):
        self.functions.insert( 0, "get_token_index_list" )
        return self
    def get_pos_tag_list( self ):
        self.functions.insert( 0, "get_pos_tag_list" )
        return self
    def get_depe_hti_list( self ):
        self.functions.insert( 0, "get_depe_hti_list" )
        return self
    def get_depe_label_list( self ):
        self.functions.insert( 0, "get_depe_label_list" )
        return self
    def get_pos_tag_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_str_list" )
        return self
    def get_depe_label_str_list( self ):
        self.functions.insert( 0, "get_depe_label_str_list" )
        return self
    def get_lemma_list( self ):
        self.functions.insert( 0, "get_lemma_list" )
        return self
    def get_text_content_token_list( self ):
        self.functions.insert( 0, "get_text_content_token_list" )
        return self

    def get_sentence_index_list( self ):
        self.functions.insert( 0, "get_sentence_index_list" )
        return self
    def get_text_content_sentence_list( self ):
        self.functions.insert( 0, "get_text_content_sentence_list" )
        return self
    def get_sentence_index_of_token_index_list( self ):
        self.functions.insert( 0, "get_sentence_index_of_token_index_list" )
        return self

    def get_sentence_index_root( self ):
        self.functions.insert( 0, "get_sentence_index_root" )
        return self
    def get_pos_tag_sentence_root( self ):
        self.functions.insert( 0, "get_pos_tag_sentence_root" )
        return self
    def get_depe_hti_sentence_root( self ):
        self.functions.insert( 0, "get_depe_hti_sentence_root" )
        return self
    def get_depe_label_sentence_root( self ):
        self.functions.insert( 0, "get_depe_label_sentence_root" )
        return self
    def get_pos_tag_str_sentence_root( self ):
        self.functions.insert( 0, "get_pos_tag_str_sentence_root" )
        return self
    def get_depe_label_str_sentence_root( self ):
        self.functions.insert( 0, "get_depe_label_str_sentence_root" )
        return self
    def get_lemma_sentence_root( self ):
        self.functions.insert( 0, "get_lemma_sentence_root" )
        return self
    def get_text_content_sentence_root( self ):
        self.functions.insert( 0, "get_text_content_sentence_root" )
        return self

    def get_sentence_root_list( self ):
        self.functions.insert( 0, "get_sentence_root_list" )
        return self
    def get_pos_tag_sentence_root_list( self ):
        self.functions.insert( 0, "get_pos_tag_sentence_root_list" )
        return self
    def get_depe_hti_sentence_root_list( self ):
        self.functions.insert( 0, "get_depe_hti_sentence_root_list" )
        return self
    def get_depe_label_sentence_root_list( self ):
        self.functions.insert( 0, "get_depe_label_sentence_root_list" )
        return self
    def get_pos_tag_str_sentence_root_list( self ):
        self.functions.insert( 0, "get_pos_tag_str_sentence_root_list" )
        return self
    def get_depe_label_str_sentence_root_list( self ):
        self.functions.insert( 0, "get_depe_label_str_sentence_root_list" )
        return self
    def get_lemma_sentence_root_list( self ):
        self.functions.insert( 0, "get_lemma_sentence_root_list" )
        return self
    def get_text_content_sentence_root_list( self ):
        self.functions.insert( 0, "get_text_content_sentence_root_list" )
        return self

    def get_branch_index_list_of_sentence_index( self ):
        self.functions.insert( 0, "get_branch_index_list_of_sentence_index" )
        return self
    def get_index_list_of_equal_hti( self ):
        self.functions.insert( 0, "get_index_list_of_equal_hti" )
        return self

    def get_master_index( self ):
        self.functions.insert( 0, "get_master_index" )
        return self
    def get_pos_tag_master( self ):
        self.functions.insert( 0, "get_pos_tag_master" )
        return self
    def get_depe_hti_master( self ):
        self.functions.insert( 0, "get_depe_hti_master" )
        return self
    def get_depe_label_master( self ):
        self.functions.insert( 0, "get_depe_label_master" )
        return self
    def get_pos_tag_str_master( self ):
        self.functions.insert( 0, "get_pos_tag_str_master" )
        return self
    def get_depe_label_str_master( self ):
        self.functions.insert( 0, "get_depe_label_str_master" )
        return self
    def get_lemma_master( self ):
        self.functions.insert( 0, "get_lemma_master" )
        return self
    def get_text_content_master( self ):
        self.functions.insert( 0, "get_text_content_master" )
        return self

    def get_master_index_list( self ):
        self.functions.insert( 0, "get_master_index_list" )
        return self

    def get_slave_index_list( self ):
        self.functions.insert( 0, "get_slave_index_list" )
        return self
    def get_pos_tag_slave_index_list( self ):
        self.functions.insert( 0, "get_pos_tag_slave_index_list" )
        return self
    def get_depe_hti_slave_index_list( self ):
        self.functions.insert( 0, "get_depe_hti_slave_index_list" )
        return self
    def get_depe_label_slave_index_list( self ):
        self.functions.insert( 0, "get_depe_label_slave_index_list" )
        return self
    def get_pos_tag_str_slave_index_list( self ):
        self.functions.insert( 0, "get_pos_tag_str_slave_index_list" )
        return self
    def get_depe_label_str_slave_index_list( self ):
        self.functions.insert( 0, "get_depe_label_str_slave_index_list" )
        return self
    def get_lemma_slave_index_list( self ):
        self.functions.insert( 0, "get_lemma_slave_index_list" )
        return self
    def get_text_content_slave_index_list( self ):
        self.functions.insert( 0, "get_text_content_slave_index_list" )
        return self

    def get_slave_index_list_of_token_index_list( self ):
        self.functions.insert( 0, "get_slave_index_list_of_token_index_list" )
        return self
    def get_pos_tag_slave_index_list_of_token_index_list( self ):
        self.functions.insert( 0, "get_pos_tag_slave_index_list_of_token_index_list" )
        return self
    def get_depe_hti_slave_index_list_of_token_index_list( self ):
        self.functions.insert( 0, "get_depe_hti_slave_index_list_of_token_index_list" )
        return self
    def get_depe_label_slave_index_list_of_token_index_list( self ):
        self.functions.insert( 0, "get_depe_label_slave_index_list_of_token_index_list" )
        return self
    def get_pos_tag_str_slave_index_list_of_token_index_list( self ):
        self.functions.insert( 0, "get_pos_tag_str_slave_index_list_of_token_index_list" )
        return self
    def get_depe_label_str_slave_index_list_of_token_index_list( self ):
        self.functions.insert( 0, "get_depe_label_str_slave_index_list_of_token_index_list" )
        return self
    def get_lemma_slave_index_list_of_token_index_list( self ):
        self.functions.insert( 0, "get_lemma_slave_index_list_of_token_index_list" )
        return self
    def get_text_content_slave_index_list_of_token_index_list( self ):
        self.functions.insert( 0, "get_text_content_slave_index_list_of_token_index_list" )
        return self

    def get_branch_token_index_to_root_index_list( self ):
        self.functions.insert( 0, "get_branch_token_index_to_root_index_list" )
        return self
    def get_branch_root_index_to_token_index_list( self ):
        self.functions.insert( 0, "get_branch_root_index_to_token_index_list" )
        return self
    def get_branch_index_list( self ):
        self.functions.insert( 0, "get_branch_index_list" )
        return self
    def get_branch_root_index( self ):
        self.functions.insert( 0, "get_branch_root_index" )
        return self

    # get_pos_tag_- #
    def get_pos_tag_UNKNOWN( self ):
        self.functions.insert( 0, "get_pos_tag_UNKNOWN" )
        return self
    def get_pos_tag_ADJ( self ):
        self.functions.insert( 0, "get_pos_tag_ADJ" )
        return self
    def get_pos_tag_ADP( self ):
        self.functions.insert( 0, "get_pos_tag_ADP" )
        return self
    def get_pos_tag_ADV( self ):
        self.functions.insert( 0, "get_pos_tag_ADV" )
        return self
    def get_pos_tag_CONJ( self ):
        self.functions.insert( 0, "get_pos_tag_CONJ" )
        return self
    def get_pos_tag_DET( self ):
        self.functions.insert( 0, "get_pos_tag_DET" )
        return self
    def get_pos_tag_NOUN( self ):
        self.functions.insert( 0, "get_pos_tag_NOUN" )
        return self
    def get_pos_tag_NUM( self ):
        self.functions.insert( 0, "get_pos_tag_NUM" )
        return self
    def get_pos_tag_PRON( self ):
        self.functions.insert( 0, "get_pos_tag_PRON" )
        return self
    def get_pos_tag_PRT( self ):
        self.functions.insert( 0, "get_pos_tag_PRT" )
        return self
    def get_pos_tag_PUNCT( self ):
        self.functions.insert( 0, "get_pos_tag_PUNCT" )
        return self
    def get_pos_tag_VERB( self ):
        self.functions.insert( 0, "get_pos_tag_VERB" )
        return self
    def get_pos_tag_X( self ):
        self.functions.insert( 0, "get_pos_tag_X" )
        return self
    def get_pos_tag_AFFIX( self ):
        self.functions.insert( 0, "get_pos_tag_AFFIX" )
        return self

    # get_pos_tag_-_str #
    def get_pos_tag_UNKNOWN_str( self ):
        self.functions.insert( 0, "get_pos_tag_UNKNOWN_str" )
        return self
    def get_pos_tag_ADJ_str( self ):
        self.functions.insert( 0, "get_pos_tag_ADJ_str" )
        return self
    def get_pos_tag_ADP_str( self ):
        self.functions.insert( 0, "get_pos_tag_ADP_str" )
        return self
    def get_pos_tag_ADV_str( self ):
        self.functions.insert( 0, "get_pos_tag_ADV_str" )
        return self
    def get_pos_tag_CONJ_str( self ):
        self.functions.insert( 0, "get_pos_tag_CONJ_str" )
        return self
    def get_pos_tag_DET_str( self ):
        self.functions.insert( 0, "get_pos_tag_DET_str" )
        return self
    def get_pos_tag_NOUN_str( self ):
        self.functions.insert( 0, "get_pos_tag_NOUN_str" )
        return self
    def get_pos_tag_NUM_str( self ):
        self.functions.insert( 0, "get_pos_tag_NUM_str" )
        return self
    def get_pos_tag_PRON_str( self ):
        self.functions.insert( 0, "get_pos_tag_PRON_str" )
        return self
    def get_pos_tag_PRT_str( self ):
        self.functions.insert( 0, "get_pos_tag_PRT_str" )
        return self
    def get_pos_tag_PUNCT_str( self ):
        self.functions.insert( 0, "get_pos_tag_PUNCT_str" )
        return self
    def get_pos_tag_VERB_str( self ):
        self.functions.insert( 0, "get_pos_tag_VERB_str" )
        return self
    def get_pos_tag_X_str( self ):
        self.functions.insert( 0, "get_pos_tag_X_str" )
        return self
    def get_pos_tag_AFFIX_str( self ):
        self.functions.insert( 0, "get_pos_tag_AFFIX_str" )
        return self

    # get_pos_tag_-_list #
    def get_pos_tag_UNKNOWN_list( self ):
        self.functions.insert( 0, "get_pos_tag_UNKNOWN_list" )
        return self
    def get_pos_tag_ADJ_list( self ):
        self.functions.insert( 0, "get_pos_tag_ADJ_list" )
        return self
    def get_pos_tag_ADP_list( self ):
        self.functions.insert( 0, "get_pos_tag_ADP_list" )
        return self
    def get_pos_tag_ADV_list( self ):
        self.functions.insert( 0, "get_pos_tag_ADV_list" )
        return self
    def get_pos_tag_CONJ_list( self ):
        self.functions.insert( 0, "get_pos_tag_CONJ_list" )
        return self
    def get_pos_tag_DET_list( self ):
        self.functions.insert( 0, "get_pos_tag_DET_list" )
        return self
    def get_pos_tag_NOUN_list( self ):
        self.functions.insert( 0, "get_pos_tag_NOUN_list" )
        return self
    def get_pos_tag_NUM_list( self ):
        self.functions.insert( 0, "get_pos_tag_NUM_list" )
        return self
    def get_pos_tag_PRON_list( self ):
        self.functions.insert( 0, "get_pos_tag_PRON_list" )
        return self
    def get_pos_tag_PRT_list( self ):
        self.functions.insert( 0, "get_pos_tag_PRT_list" )
        return self
    def get_pos_tag_PUNCT_list( self ):
        self.functions.insert( 0, "get_pos_tag_PUNCT_list" )
        return self
    def get_pos_tag_VERB_list( self ):
        self.functions.insert( 0, "get_pos_tag_VERB_list" )
        return self
    def get_pos_tag_X_list( self ):
        self.functions.insert( 0, "get_pos_tag_X_list" )
        return self
    def get_pos_tag_AFFIX_list( self ):
        self.functions.insert( 0, "get_pos_tag_AFFIX_list" )
        return self

    # get_pos_tag_-_str_list #
    def get_pos_tag_UNKNOWN_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_UNKNOWN_str_list" )
        return self
    def get_pos_tag_ADJ_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_ADJ_str_list" )
        return self
    def get_pos_tag_ADP_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_ADP_str_list" )
        return self
    def get_pos_tag_ADV_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_ADV_str_list" )
        return self
    def get_pos_tag_CONJ_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_CONJ_str_list" )
        return self
    def get_pos_tag_DET_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_DET_str_list" )
        return self
    def get_pos_tag_NOUN_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_NOUN_str_list" )
        return self
    def get_pos_tag_NUM_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_NUM_str_list" )
        return self
    def get_pos_tag_PRON_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_PRON_str_list" )
        return self
    def get_pos_tag_PRT_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_PRT_str_list" )
        return self
    def get_pos_tag_PUNCT_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_PUNCT_str_list" )
        return self
    def get_pos_tag_VERB_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_VERB_str_list" )
        return self
    def get_pos_tag_X_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_X_str_list" )
        return self
    def get_pos_tag_AFFIX_str_list( self ):
        self.functions.insert( 0, "get_pos_tag_AFFIX_str_list" )
        return self


    # get_depe_label_- #
    def get_depe_label_UNKNOWN( self ):
        self.functions.insert( 0, "get_depe_label_UNKNOWN" )
        return self
    def get_depe_label_ABBREV( self ):
        self.functions.insert( 0, "get_depe_label_ABBREV" )
        return self
    def get_depe_label_ACOMP( self ):
        self.functions.insert( 0, "get_depe_label_ACOMP" )
        return self
    def get_depe_label_ADVCL( self ):
        self.functions.insert( 0, "get_depe_label_ADVCL" )
        return self
    def get_depe_label_ADVMOD( self ):
        self.functions.insert( 0, "get_depe_label_ADVMOD" )
        return self
    def get_depe_label_AMOD( self ):
        self.functions.insert( 0, "get_depe_label_AMOD" )
        return self
    def get_depe_label_APPOS( self ):
        self.functions.insert( 0, "get_depe_label_APPOS" )
        return self
    def get_depe_label_ATTR( self ):
        self.functions.insert( 0, "get_depe_label_ATTR" )
        return self
    def get_depe_label_AUX( self ):
        self.functions.insert( 0, "get_depe_label_AUX" )
        return self
    def get_depe_label_AUXPASS( self ):
        self.functions.insert( 0, "get_depe_label_AUXPASS" )
        return self
    def get_depe_label_CC( self ):
        self.functions.insert( 0, "get_depe_label_CC" )
        return self
    def get_depe_label_CCOMP( self ):
        self.functions.insert( 0, "get_depe_label_CCOMP" )
        return self
    def get_depe_label_CONJ( self ):
        self.functions.insert( 0, "get_depe_label_CONJ" )
        return self
    def get_depe_label_CSUBJ( self ):
        self.functions.insert( 0, "get_depe_label_CSUBJ" )
        return self
    def get_depe_label_CSUBJPASS( self ):
        self.functions.insert( 0, "get_depe_label_CSUBJPASS" )
        return self
    def get_depe_label_DEP( self ):
        self.functions.insert( 0, "get_depe_label_DEP" )
        return self
    def get_depe_label_DET( self ):
        self.functions.insert( 0, "get_depe_label_DET" )
        return self
    def get_depe_label_DISCOURSE( self ):
        self.functions.insert( 0, "get_depe_label_DISCOURSE" )
        return self
    def get_depe_label_DOBJ( self ):
        self.functions.insert( 0, "get_depe_label_DOBJ" )
        return self
    def get_depe_label_EXPL( self ):
        self.functions.insert( 0, "get_depe_label_EXPL" )
        return self
    def get_depe_label_GOESWITH( self ):
        self.functions.insert( 0, "get_depe_label_GOESWITH" )
        return self
    def get_depe_label_IOBJ( self ):
        self.functions.insert( 0, "get_depe_label_IOBJ" )
        return self
    def get_depe_label_MARK( self ):
        self.functions.insert( 0, "get_depe_label_MARK" )
        return self
    def get_depe_label_MWE( self ):
        self.functions.insert( 0, "get_depe_label_MWE" )
        return self
    def get_depe_label_MWV( self ):
        self.functions.insert( 0, "get_depe_label_MWV" )
        return self
    def get_depe_label_NEG( self ):
        self.functions.insert( 0, "get_depe_label_NEG" )
        return self
    def get_depe_label_NN( self ):
        self.functions.insert( 0, "get_depe_label_NN" )
        return self
    def get_depe_label_NPADVMOD( self ):
        self.functions.insert( 0, "get_depe_label_NPADVMOD" )
        return self
    def get_depe_label_NSUBJ( self ):
        self.functions.insert( 0, "get_depe_label_NSUBJ" )
        return self
    def get_depe_label_NSUBJPASS( self ):
        self.functions.insert( 0, "get_depe_label_NSUBJPASS" )
        return self
    def get_depe_label_NUM( self ):
        self.functions.insert( 0, "get_depe_label_NUM" )
        return self
    def get_depe_label_NUMBER( self ):
        self.functions.insert( 0, "get_depe_label_NUMBER" )
        return self
    def get_depe_label_P( self ):
        self.functions.insert( 0, "get_depe_label_P" )
        return self
    def get_depe_label_PARATAXIS( self ):
        self.functions.insert( 0, "get_depe_label_PARATAXIS" )
        return self
    def get_depe_label_PARTMOD( self ):
        self.functions.insert( 0, "get_depe_label_PARTMOD" )
        return self
    def get_depe_label_PCOMP( self ):
        self.functions.insert( 0, "get_depe_label_PCOMP" )
        return self
    def get_depe_label_POBJ( self ):
        self.functions.insert( 0, "get_depe_label_POBJ" )
        return self
    def get_depe_label_POSS( self ):
        self.functions.insert( 0, "get_depe_label_POSS" )
        return self
    def get_depe_label_POSTNEG( self ):
        self.functions.insert( 0, "get_depe_label_POSTNEG" )
        return self
    def get_depe_label_PRECOMP( self ):
        self.functions.insert( 0, "get_depe_label_PRECOMP" )
        return self
    def get_depe_label_PRECONJ( self ):
        self.functions.insert( 0, "get_depe_label_PRECONJ" )
        return self
    def get_depe_label_PREDET( self ):
        self.functions.insert( 0, "get_depe_label_PREDET" )
        return self
    def get_depe_label_PREF( self ):
        self.functions.insert( 0, "get_depe_label_PREF" )
        return self
    def get_depe_label_PREP( self ):
        self.functions.insert( 0, "get_depe_label_PREP" )
        return self
    def get_depe_label_PRONL( self ):
        self.functions.insert( 0, "get_depe_label_PRONL" )
        return self
    def get_depe_label_PRT( self ):
        self.functions.insert( 0, "get_depe_label_PRT" )
        return self
    def get_depe_label_PS( self ):
        self.functions.insert( 0, "get_depe_label_PS" )
        return self
    def get_depe_label_QUANTMOD( self ):
        self.functions.insert( 0, "get_depe_label_QUANTMOD" )
        return self
    def get_depe_label_RCMOD( self ):
        self.functions.insert( 0, "get_depe_label_RCMOD" )
        return self
    def get_depe_label_RCMODREL( self ):
        self.functions.insert( 0, "get_depe_label_RCMODREL" )
        return self
    def get_depe_label_RDROP( self ):
        self.functions.insert( 0, "get_depe_label_RDROP" )
        return self
    def get_depe_label_REF( self ):
        self.functions.insert( 0, "get_depe_label_REF" )
        return self
    def get_depe_label_REMNANT( self ):
        self.functions.insert( 0, "get_depe_label_REMNANT" )
        return self
    def get_depe_label_REPARANDUM( self ):
        self.functions.insert( 0, "get_depe_label_REPARANDUM" )
        return self
    def get_depe_label_ROOT( self ):
        self.functions.insert( 0, "get_depe_label_ROOT" )
        return self
    def get_depe_label_SNUM( self ):
        self.functions.insert( 0, "get_depe_label_SNUM" )
        return self
    def get_depe_label_SUFF( self ):
        self.functions.insert( 0, "get_depe_label_SUFF" )
        return self
    def get_depe_label_TMOD( self ):
        self.functions.insert( 0, "get_depe_label_TMOD" )
        return self
    def get_depe_label_TOPIC( self ):
        self.functions.insert( 0, "get_depe_label_TOPIC" )
        return self
    def get_depe_label_VMOD( self ):
        self.functions.insert( 0, "get_depe_label_VMOD" )
        return self
    def get_depe_label_VOCATIVE( self ):
        self.functions.insert( 0, "get_depe_label_VOCATIVE" )
        return self
    def get_depe_label_XCOMP( self ):
        self.functions.insert( 0, "get_depe_label_XCOMP" )
        return self
    def get_depe_label_SUFFIX( self ):
        self.functions.insert( 0, "get_depe_label_SUFFIX" )
        return self
    def get_depe_label_TITLE( self ):
        self.functions.insert( 0, "get_depe_label_TITLE" )
        return self
    def get_depe_label_ADVPHMOD( self ):
        self.functions.insert( 0, "get_depe_label_ADVPHMOD" )
        return self
    def get_depe_label_AUXCAUS( self ):
        self.functions.insert( 0, "get_depe_label_AUXCAUS" )
        return self
    def get_depe_label_AUXVV( self ):
        self.functions.insert( 0, "get_depe_label_AUXVV" )
        return self
    def get_depe_label_DTMOD( self ):
        self.functions.insert( 0, "get_depe_label_DTMOD" )
        return self
    def get_depe_label_FOREIGN( self ):
        self.functions.insert( 0, "get_depe_label_FOREIGN" )
        return self
    def get_depe_label_KW( self ):
        self.functions.insert( 0, "get_depe_label_KW" )
        return self
    def get_depe_label_LIST( self ):
        self.functions.insert( 0, "get_depe_label_LIST" )
        return self
    def get_depe_label_NOMC( self ):
        self.functions.insert( 0, "get_depe_label_NOMC" )
        return self
    def get_depe_label_NOMCSUBJ( self ):
        self.functions.insert( 0, "get_depe_label_NOMCSUBJ" )
        return self
    def get_depe_label_NOMCSUBJPASS( self ):
        self.functions.insert( 0, "get_depe_label_NOMCSUBJPASS" )
        return self
    def get_depe_label_NUMC( self ):
        self.functions.insert( 0, "get_depe_label_NUMC" )
        return self
    def get_depe_label_COP( self ):
        self.functions.insert( 0, "get_depe_label_COP" )
        return self
    def get_depe_label_DISLOCATED( self ):
        self.functions.insert( 0, "get_depe_label_DISLOCATED" )
        return self

    # get_depe_label_-_str #
    def get_depe_label_UNKNOWN_str( self ):
        self.functions.insert( 0, "get_depe_label_UNKNOWN_str" )
        return self
    def get_depe_label_ABBREV_str( self ):
        self.functions.insert( 0, "get_depe_label_ABBREV_str" )
        return self
    def get_depe_label_ACOMP_str( self ):
        self.functions.insert( 0, "get_depe_label_ACOMP_str" )
        return self
    def get_depe_label_ADVCL_str( self ):
        self.functions.insert( 0, "get_depe_label_ADVCL_str" )
        return self
    def get_depe_label_ADVMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_ADVMOD_str" )
        return self
    def get_depe_label_AMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_AMOD_str" )
        return self
    def get_depe_label_APPOS_str( self ):
        self.functions.insert( 0, "get_depe_label_APPOS_str" )
        return self
    def get_depe_label_ATTR_str( self ):
        self.functions.insert( 0, "get_depe_label_ATTR_str" )
        return self
    def get_depe_label_AUX_str( self ):
        self.functions.insert( 0, "get_depe_label_AUX_str" )
        return self
    def get_depe_label_AUXPASS_str( self ):
        self.functions.insert( 0, "get_depe_label_AUXPASS_str" )
        return self
    def get_depe_label_CC_str( self ):
        self.functions.insert( 0, "get_depe_label_CC_str" )
        return self
    def get_depe_label_CCOMP_str( self ):
        self.functions.insert( 0, "get_depe_label_CCOMP_str" )
        return self
    def get_depe_label_CONJ_str( self ):
        self.functions.insert( 0, "get_depe_label_CONJ_str" )
        return self
    def get_depe_label_CSUBJ_str( self ):
        self.functions.insert( 0, "get_depe_label_CSUBJ_str" )
        return self
    def get_depe_label_CSUBJPASS_str( self ):
        self.functions.insert( 0, "get_depe_label_CSUBJPASS_str" )
        return self
    def get_depe_label_DEP_str( self ):
        self.functions.insert( 0, "get_depe_label_DEP_str" )
        return self
    def get_depe_label_DET_str( self ):
        self.functions.insert( 0, "get_depe_label_DET_str" )
        return self
    def get_depe_label_DISCOURSE_str( self ):
        self.functions.insert( 0, "get_depe_label_DISCOURSE_str" )
        return self
    def get_depe_label_DOBJ_str( self ):
        self.functions.insert( 0, "get_depe_label_DOBJ_str" )
        return self
    def get_depe_label_EXPL_str( self ):
        self.functions.insert( 0, "get_depe_label_EXPL_str" )
        return self
    def get_depe_label_GOESWITH_str( self ):
        self.functions.insert( 0, "get_depe_label_GOESWITH_str" )
        return self
    def get_depe_label_IOBJ_str( self ):
        self.functions.insert( 0, "get_depe_label_IOBJ_str" )
        return self
    def get_depe_label_MARK_str( self ):
        self.functions.insert( 0, "get_depe_label_MARK_str" )
        return self
    def get_depe_label_MWE_str( self ):
        self.functions.insert( 0, "get_depe_label_MWE_str" )
        return self
    def get_depe_label_MWV_str( self ):
        self.functions.insert( 0, "get_depe_label_MWV_str" )
        return self
    def get_depe_label_NEG_str( self ):
        self.functions.insert( 0, "get_depe_label_NEG_str" )
        return self
    def get_depe_label_NN_str( self ):
        self.functions.insert( 0, "get_depe_label_NN_str" )
        return self
    def get_depe_label_NPADVMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_NPADVMOD_str" )
        return self
    def get_depe_label_NSUBJ_str( self ):
        self.functions.insert( 0, "get_depe_label_NSUBJ_str" )
        return self
    def get_depe_label_NSUBJPASS_str( self ):
        self.functions.insert( 0, "get_depe_label_NSUBJPASS_str" )
        return self
    def get_depe_label_NUM_str( self ):
        self.functions.insert( 0, "get_depe_label_NUM_str" )
        return self
    def get_depe_label_NUMBER_str( self ):
        self.functions.insert( 0, "get_depe_label_NUMBER_str" )
        return self
    def get_depe_label_P_str( self ):
        self.functions.insert( 0, "get_depe_label_P_str" )
        return self
    def get_depe_label_PARATAXIS_str( self ):
        self.functions.insert( 0, "get_depe_label_PARATAXIS_str" )
        return self
    def get_depe_label_PARTMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_PARTMOD_str" )
        return self
    def get_depe_label_PCOMP_str( self ):
        self.functions.insert( 0, "get_depe_label_PCOMP_str" )
        return self
    def get_depe_label_POBJ_str( self ):
        self.functions.insert( 0, "get_depe_label_POBJ_str" )
        return self
    def get_depe_label_POSS_str( self ):
        self.functions.insert( 0, "get_depe_label_POSS_str" )
        return self
    def get_depe_label_POSTNEG_str( self ):
        self.functions.insert( 0, "get_depe_label_POSTNEG_str" )
        return self
    def get_depe_label_PRECOMP_str( self ):
        self.functions.insert( 0, "get_depe_label_PRECOMP_str" )
        return self
    def get_depe_label_PRECONJ_str( self ):
        self.functions.insert( 0, "get_depe_label_PRECONJ_str" )
        return self
    def get_depe_label_PREDET_str( self ):
        self.functions.insert( 0, "get_depe_label_PREDET_str" )
        return self
    def get_depe_label_PREF_str( self ):
        self.functions.insert( 0, "get_depe_label_PREF_str" )
        return self
    def get_depe_label_PREP_str( self ):
        self.functions.insert( 0, "get_depe_label_PREP_str" )
        return self
    def get_depe_label_PRONL_str( self ):
        self.functions.insert( 0, "get_depe_label_PRONL_str" )
        return self
    def get_depe_label_PRT_str( self ):
        self.functions.insert( 0, "get_depe_label_PRT_str" )
        return self
    def get_depe_label_PS_str( self ):
        self.functions.insert( 0, "get_depe_label_PS_str" )
        return self
    def get_depe_label_QUANTMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_QUANTMOD_str" )
        return self
    def get_depe_label_RCMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_RCMOD_str" )
        return self
    def get_depe_label_RCMODREL_str( self ):
        self.functions.insert( 0, "get_depe_label_RCMODREL_str" )
        return self
    def get_depe_label_RDROP_str( self ):
        self.functions.insert( 0, "get_depe_label_RDROP_str" )
        return self
    def get_depe_label_REF_str( self ):
        self.functions.insert( 0, "get_depe_label_REF_str" )
        return self
    def get_depe_label_REMNANT_str( self ):
        self.functions.insert( 0, "get_depe_label_REMNANT_str" )
        return self
    def get_depe_label_REPARANDUM_str( self ):
        self.functions.insert( 0, "get_depe_label_REPARANDUM_str" )
        return self
    def get_depe_label_ROOT_str( self ):
        self.functions.insert( 0, "get_depe_label_ROOT_str" )
        return self
    def get_depe_label_SNUM_str( self ):
        self.functions.insert( 0, "get_depe_label_SNUM_str" )
        return self
    def get_depe_label_SUFF_str( self ):
        self.functions.insert( 0, "get_depe_label_SUFF_str" )
        return self
    def get_depe_label_TMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_TMOD_str" )
        return self
    def get_depe_label_TOPIC_str( self ):
        self.functions.insert( 0, "get_depe_label_TOPIC_str" )
        return self
    def get_depe_label_VMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_VMOD_str" )
        return self
    def get_depe_label_VOCATIVE_str( self ):
        self.functions.insert( 0, "get_depe_label_VOCATIVE_str" )
        return self
    def get_depe_label_XCOMP_str( self ):
        self.functions.insert( 0, "get_depe_label_XCOMP_str" )
        return self
    def get_depe_label_SUFFIX_str( self ):
        self.functions.insert( 0, "get_depe_label_SUFFIX_str" )
        return self
    def get_depe_label_TITLE_str( self ):
        self.functions.insert( 0, "get_depe_label_TITLE_str" )
        return self
    def get_depe_label_ADVPHMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_ADVPHMOD_str" )
        return self
    def get_depe_label_AUXCAUS_str( self ):
        self.functions.insert( 0, "get_depe_label_AUXCAUS_str" )
        return self
    def get_depe_label_AUXVV_str( self ):
        self.functions.insert( 0, "get_depe_label_AUXVV_str" )
        return self
    def get_depe_label_DTMOD_str( self ):
        self.functions.insert( 0, "get_depe_label_DTMOD_str" )
        return self
    def get_depe_label_FOREIGN_str( self ):
        self.functions.insert( 0, "get_depe_label_FOREIGN_str" )
        return self
    def get_depe_label_KW_str( self ):
        self.functions.insert( 0, "get_depe_label_KW_str" )
        return self
    def get_depe_label_LIST_str( self ):
        self.functions.insert( 0, "get_depe_label_LIST_str" )
        return self
    def get_depe_label_NOMC_str( self ):
        self.functions.insert( 0, "get_depe_label_NOMC_str" )
        return self
    def get_depe_label_NOMCSUBJ_str( self ):
        self.functions.insert( 0, "get_depe_label_NOMCSUBJ_str" )
        return self
    def get_depe_label_NOMCSUBJPASS_str( self ):
        self.functions.insert( 0, "get_depe_label_NOMCSUBJPASS_str" )
        return self
    def get_depe_label_NUMC_str( self ):
        self.functions.insert( 0, "get_depe_label_NUMC_str" )
        return self
    def get_depe_label_COP_str( self ):
        self.functions.insert( 0, "get_depe_label_COP_str" )
        return self
    def get_depe_label_DISLOCATED_str( self ):
        self.functions.insert( 0, "get_depe_label_DISLOCATED_str" )
        return self

    # get_depe_label_-_list #
    def get_depe_label_UNKNOWN_list( self ):
        self.functions.insert( 0, "get_depe_label_UNKNOWN_list" )
        return self
    def get_depe_label_ABBREV_list( self ):
        self.functions.insert( 0, "get_depe_label_ABBREV_list" )
        return self
    def get_depe_label_ACOMP_list( self ):
        self.functions.insert( 0, "get_depe_label_ACOMP_list" )
        return self
    def get_depe_label_ADVCL_list( self ):
        self.functions.insert( 0, "get_depe_label_ADVCL_list" )
        return self
    def get_depe_label_ADVMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_ADVMOD_list" )
        return self
    def get_depe_label_AMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_AMOD_list" )
        return self
    def get_depe_label_APPOS_list( self ):
        self.functions.insert( 0, "get_depe_label_APPOS_list" )
        return self
    def get_depe_label_ATTR_list( self ):
        self.functions.insert( 0, "get_depe_label_ATTR_list" )
        return self
    def get_depe_label_AUX_list( self ):
        self.functions.insert( 0, "get_depe_label_AUX_list" )
        return self
    def get_depe_label_AUXPASS_list( self ):
        self.functions.insert( 0, "get_depe_label_AUXPASS_list" )
        return self
    def get_depe_label_CC_list( self ):
        self.functions.insert( 0, "get_depe_label_CC_list" )
        return self
    def get_depe_label_CCOMP_list( self ):
        self.functions.insert( 0, "get_depe_label_CCOMP_list" )
        return self
    def get_depe_label_CONJ_list( self ):
        self.functions.insert( 0, "get_depe_label_CONJ_list" )
        return self
    def get_depe_label_CSUBJ_list( self ):
        self.functions.insert( 0, "get_depe_label_CSUBJ_list" )
        return self
    def get_depe_label_CSUBJPASS_list( self ):
        self.functions.insert( 0, "get_depe_label_CSUBJPASS_list" )
        return self
    def get_depe_label_DEP_list( self ):
        self.functions.insert( 0, "get_depe_label_DEP_list" )
        return self
    def get_depe_label_DET_list( self ):
        self.functions.insert( 0, "get_depe_label_DET_list" )
        return self
    def get_depe_label_DISCOURSE_list( self ):
        self.functions.insert( 0, "get_depe_label_DISCOURSE_list" )
        return self
    def get_depe_label_DOBJ_list( self ):
        self.functions.insert( 0, "get_depe_label_DOBJ_list" )
        return self
    def get_depe_label_EXPL_list( self ):
        self.functions.insert( 0, "get_depe_label_EXPL_list" )
        return self
    def get_depe_label_GOESWITH_list( self ):
        self.functions.insert( 0, "get_depe_label_GOESWITH_list" )
        return self
    def get_depe_label_IOBJ_list( self ):
        self.functions.insert( 0, "get_depe_label_IOBJ_list" )
        return self
    def get_depe_label_MARK_list( self ):
        self.functions.insert( 0, "get_depe_label_MARK_list" )
        return self
    def get_depe_label_MWE_list( self ):
        self.functions.insert( 0, "get_depe_label_MWE_list" )
        return self
    def get_depe_label_MWV_list( self ):
        self.functions.insert( 0, "get_depe_label_MWV_list" )
        return self
    def get_depe_label_NEG_list( self ):
        self.functions.insert( 0, "get_depe_label_NEG_list" )
        return self
    def get_depe_label_NN_list( self ):
        self.functions.insert( 0, "get_depe_label_NN_list" )
        return self
    def get_depe_label_NPADVMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_NPADVMOD_list" )
        return self
    def get_depe_label_NSUBJ_list( self ):
        self.functions.insert( 0, "get_depe_label_NSUBJ_list" )
        return self
    def get_depe_label_NSUBJPASS_list( self ):
        self.functions.insert( 0, "get_depe_label_NSUBJPASS_list" )
        return self
    def get_depe_label_NUM_list( self ):
        self.functions.insert( 0, "get_depe_label_NUM_list" )
        return self
    def get_depe_label_NUMBER_list( self ):
        self.functions.insert( 0, "get_depe_label_NUMBER_list" )
        return self
    def get_depe_label_P_list( self ):
        self.functions.insert( 0, "get_depe_label_P_list" )
        return self
    def get_depe_label_PARATAXIS_list( self ):
        self.functions.insert( 0, "get_depe_label_PARATAXIS_list" )
        return self
    def get_depe_label_PARTMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_PARTMOD_list" )
        return self
    def get_depe_label_PCOMP_list( self ):
        self.functions.insert( 0, "get_depe_label_PCOMP_list" )
        return self
    def get_depe_label_POBJ_list( self ):
        self.functions.insert( 0, "get_depe_label_POBJ_list" )
        return self
    def get_depe_label_POSS_list( self ):
        self.functions.insert( 0, "get_depe_label_POSS_list" )
        return self
    def get_depe_label_POSTNEG_list( self ):
        self.functions.insert( 0, "get_depe_label_POSTNEG_list" )
        return self
    def get_depe_label_PRECOMP_list( self ):
        self.functions.insert( 0, "get_depe_label_PRECOMP_list" )
        return self
    def get_depe_label_PRECONJ_list( self ):
        self.functions.insert( 0, "get_depe_label_PRECONJ_list" )
        return self
    def get_depe_label_PREDET_list( self ):
        self.functions.insert( 0, "get_depe_label_PREDET_list" )
        return self
    def get_depe_label_PREF_list( self ):
        self.functions.insert( 0, "get_depe_label_PREF_list" )
        return self
    def get_depe_label_PREP_list( self ):
        self.functions.insert( 0, "get_depe_label_PREP_list" )
        return self
    def get_depe_label_PRONL_list( self ):
        self.functions.insert( 0, "get_depe_label_PRONL_list" )
        return self
    def get_depe_label_PRT_list( self ):
        self.functions.insert( 0, "get_depe_label_PRT_list" )
        return self
    def get_depe_label_PS_list( self ):
        self.functions.insert( 0, "get_depe_label_PS_list" )
        return self
    def get_depe_label_QUANTMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_QUANTMOD_list" )
        return self
    def get_depe_label_RCMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_RCMOD_list" )
        return self
    def get_depe_label_RCMODREL_list( self ):
        self.functions.insert( 0, "get_depe_label_RCMODREL_list" )
        return self
    def get_depe_label_RDROP_list( self ):
        self.functions.insert( 0, "get_depe_label_RDROP_list" )
        return self
    def get_depe_label_REF_list( self ):
        self.functions.insert( 0, "get_depe_label_REF_list" )
        return self
    def get_depe_label_REMNANT_list( self ):
        self.functions.insert( 0, "get_depe_label_REMNANT_list" )
        return self
    def get_depe_label_REPARANDUM_list( self ):
        self.functions.insert( 0, "get_depe_label_REPARANDUM_list" )
        return self
    def get_depe_label_ROOT_list( self ):
        self.functions.insert( 0, "get_depe_label_ROOT_list" )
        return self
    def get_depe_label_SNUM_list( self ):
        self.functions.insert( 0, "get_depe_label_SNUM_list" )
        return self
    def get_depe_label_SUFF_list( self ):
        self.functions.insert( 0, "get_depe_label_SUFF_list" )
        return self
    def get_depe_label_TMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_TMOD_list" )
        return self
    def get_depe_label_TOPIC_list( self ):
        self.functions.insert( 0, "get_depe_label_TOPIC_list" )
        return self
    def get_depe_label_VMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_VMOD_list" )
        return self
    def get_depe_label_VOCATIVE_list( self ):
        self.functions.insert( 0, "get_depe_label_VOCATIVE_list" )
        return self
    def get_depe_label_XCOMP_list( self ):
        self.functions.insert( 0, "get_depe_label_XCOMP_list" )
        return self
    def get_depe_label_SUFFIX_list( self ):
        self.functions.insert( 0, "get_depe_label_SUFFIX_list" )
        return self
    def get_depe_label_TITLE_list( self ):
        self.functions.insert( 0, "get_depe_label_TITLE_list" )
        return self
    def get_depe_label_ADVPHMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_ADVPHMOD_list" )
        return self
    def get_depe_label_AUXCAUS_list( self ):
        self.functions.insert( 0, "get_depe_label_AUXCAUS_list" )
        return self
    def get_depe_label_AUXVV_list( self ):
        self.functions.insert( 0, "get_depe_label_AUXVV_list" )
        return self
    def get_depe_label_DTMOD_list( self ):
        self.functions.insert( 0, "get_depe_label_DTMOD_list" )
        return self
    def get_depe_label_FOREIGN_list( self ):
        self.functions.insert( 0, "get_depe_label_FOREIGN_list" )
        return self
    def get_depe_label_KW_list( self ):
        self.functions.insert( 0, "get_depe_label_KW_list" )
        return self
    def get_depe_label_LIST_list( self ):
        self.functions.insert( 0, "get_depe_label_LIST_list" )
        return self
    def get_depe_label_NOMC_list( self ):
        self.functions.insert( 0, "get_depe_label_NOMC_list" )
        return self
    def get_depe_label_NOMCSUBJ_list( self ):
        self.functions.insert( 0, "get_depe_label_NOMCSUBJ_list" )
        return self
    def get_depe_label_NOMCSUBJPASS_list( self ):
        self.functions.insert( 0, "get_depe_label_NOMCSUBJPASS_list" )
        return self
    def get_depe_label_NUMC_list( self ):
        self.functions.insert( 0, "get_depe_label_NUMC_list" )
        return self
    def get_depe_label_COP_list( self ):
        self.functions.insert( 0, "get_depe_label_COP_list" )
        return self
    def get_depe_label_DISLOCATED_list( self ):
        self.functions.insert( 0, "get_depe_label_DISLOCATED_list" )
        return self

    # get_depe_label_-_str_list #
    def get_depe_label_UNKNOWN_str_list( self ):
        self.functions.insert( 0, "get_depe_label_UNKNOWN_str_list" )
        return self
    def get_depe_label_ABBREV_str_list( self ):
        self.functions.insert( 0, "get_depe_label_ABBREV_str_list" )
        return self
    def get_depe_label_ACOMP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_ACOMP_str_list" )
        return self
    def get_depe_label_ADVCL_str_list( self ):
        self.functions.insert( 0, "get_depe_label_ADVCL_str_list" )
        return self
    def get_depe_label_ADVMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_ADVMOD_str_list" )
        return self
    def get_depe_label_AMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_AMOD_str_list" )
        return self
    def get_depe_label_APPOS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_APPOS_str_list" )
        return self
    def get_depe_label_ATTR_str_list( self ):
        self.functions.insert( 0, "get_depe_label_ATTR_str_list" )
        return self
    def get_depe_label_AUX_str_list( self ):
        self.functions.insert( 0, "get_depe_label_AUX_str_list" )
        return self
    def get_depe_label_AUXPASS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_AUXPASS_str_list" )
        return self
    def get_depe_label_CC_str_list( self ):
        self.functions.insert( 0, "get_depe_label_CC_str_list" )
        return self
    def get_depe_label_CCOMP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_CCOMP_str_list" )
        return self
    def get_depe_label_CONJ_str_list( self ):
        self.functions.insert( 0, "get_depe_label_CONJ_str_list" )
        return self
    def get_depe_label_CSUBJ_str_list( self ):
        self.functions.insert( 0, "get_depe_label_CSUBJ_str_list" )
        return self
    def get_depe_label_CSUBJPASS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_CSUBJPASS_str_list" )
        return self
    def get_depe_label_DEP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_DEP_str_list" )
        return self
    def get_depe_label_DET_str_list( self ):
        self.functions.insert( 0, "get_depe_label_DET_str_list" )
        return self
    def get_depe_label_DISCOURSE_str_list( self ):
        self.functions.insert( 0, "get_depe_label_DISCOURSE_str_list" )
        return self
    def get_depe_label_DOBJ_str_list( self ):
        self.functions.insert( 0, "get_depe_label_DOBJ_str_list" )
        return self
    def get_depe_label_EXPL_str_list( self ):
        self.functions.insert( 0, "get_depe_label_EXPL_str_list" )
        return self
    def get_depe_label_GOESWITH_str_list( self ):
        self.functions.insert( 0, "get_depe_label_GOESWITH_str_list" )
        return self
    def get_depe_label_IOBJ_str_list( self ):
        self.functions.insert( 0, "get_depe_label_IOBJ_str_list" )
        return self
    def get_depe_label_MARK_str_list( self ):
        self.functions.insert( 0, "get_depe_label_MARK_str_list" )
        return self
    def get_depe_label_MWE_str_list( self ):
        self.functions.insert( 0, "get_depe_label_MWE_str_list" )
        return self
    def get_depe_label_MWV_str_list( self ):
        self.functions.insert( 0, "get_depe_label_MWV_str_list" )
        return self
    def get_depe_label_NEG_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NEG_str_list" )
        return self
    def get_depe_label_NN_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NN_str_list" )
        return self
    def get_depe_label_NPADVMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NPADVMOD_str_list" )
        return self
    def get_depe_label_NSUBJ_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NSUBJ_str_list" )
        return self
    def get_depe_label_NSUBJPASS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NSUBJPASS_str_list" )
        return self
    def get_depe_label_NUM_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NUM_str_list" )
        return self
    def get_depe_label_NUMBER_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NUMBER_str_list" )
        return self
    def get_depe_label_P_str_list( self ):
        self.functions.insert( 0, "get_depe_label_P_str_list" )
        return self
    def get_depe_label_PARATAXIS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PARATAXIS_str_list" )
        return self
    def get_depe_label_PARTMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PARTMOD_str_list" )
        return self
    def get_depe_label_PCOMP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PCOMP_str_list" )
        return self
    def get_depe_label_POBJ_str_list( self ):
        self.functions.insert( 0, "get_depe_label_POBJ_str_list" )
        return self
    def get_depe_label_POSS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_POSS_str_list" )
        return self
    def get_depe_label_POSTNEG_str_list( self ):
        self.functions.insert( 0, "get_depe_label_POSTNEG_str_list" )
        return self
    def get_depe_label_PRECOMP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PRECOMP_str_list" )
        return self
    def get_depe_label_PRECONJ_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PRECONJ_str_list" )
        return self
    def get_depe_label_PREDET_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PREDET_str_list" )
        return self
    def get_depe_label_PREF_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PREF_str_list" )
        return self
    def get_depe_label_PREP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PREP_str_list" )
        return self
    def get_depe_label_PRONL_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PRONL_str_list" )
        return self
    def get_depe_label_PRT_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PRT_str_list" )
        return self
    def get_depe_label_PS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_PS_str_list" )
        return self
    def get_depe_label_QUANTMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_QUANTMOD_str_list" )
        return self
    def get_depe_label_RCMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_RCMOD_str_list" )
        return self
    def get_depe_label_RCMODREL_str_list( self ):
        self.functions.insert( 0, "get_depe_label_RCMODREL_str_list" )
        return self
    def get_depe_label_RDROP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_RDROP_str_list" )
        return self
    def get_depe_label_REF_str_list( self ):
        self.functions.insert( 0, "get_depe_label_REF_str_list" )
        return self
    def get_depe_label_REMNANT_str_list( self ):
        self.functions.insert( 0, "get_depe_label_REMNANT_str_list" )
        return self
    def get_depe_label_REPARANDUM_str_list( self ):
        self.functions.insert( 0, "get_depe_label_REPARANDUM_str_list" )
        return self
    def get_depe_label_ROOT_str_list( self ):
        self.functions.insert( 0, "get_depe_label_ROOT_str_list" )
        return self
    def get_depe_label_SNUM_str_list( self ):
        self.functions.insert( 0, "get_depe_label_SNUM_str_list" )
        return self
    def get_depe_label_SUFF_str_list( self ):
        self.functions.insert( 0, "get_depe_label_SUFF_str_list" )
        return self
    def get_depe_label_TMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_TMOD_str_list" )
        return self
    def get_depe_label_TOPIC_str_list( self ):
        self.functions.insert( 0, "get_depe_label_TOPIC_str_list" )
        return self
    def get_depe_label_VMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_VMOD_str_list" )
        return self
    def get_depe_label_VOCATIVE_str_list( self ):
        self.functions.insert( 0, "get_depe_label_VOCATIVE_str_list" )
        return self
    def get_depe_label_XCOMP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_XCOMP_str_list" )
        return self
    def get_depe_label_SUFFIX_str_list( self ):
        self.functions.insert( 0, "get_depe_label_SUFFIX_str_list" )
        return self
    def get_depe_label_TITLE_str_list( self ):
        self.functions.insert( 0, "get_depe_label_TITLE_str_list" )
        return self
    def get_depe_label_ADVPHMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_ADVPHMOD_str_list" )
        return self
    def get_depe_label_AUXCAUS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_AUXCAUS_str_list" )
        return self
    def get_depe_label_AUXVV_str_list( self ):
        self.functions.insert( 0, "get_depe_label_AUXVV_str_list" )
        return self
    def get_depe_label_DTMOD_str_list( self ):
        self.functions.insert( 0, "get_depe_label_DTMOD_str_list" )
        return self
    def get_depe_label_FOREIGN_str_list( self ):
        self.functions.insert( 0, "get_depe_label_FOREIGN_str_list" )
        return self
    def get_depe_label_KW_str_list( self ):
        self.functions.insert( 0, "get_depe_label_KW_str_list" )
        return self
    def get_depe_label_LIST_str_list( self ):
        self.functions.insert( 0, "get_depe_label_LIST_str_list" )
        return self
    def get_depe_label_NOMC_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NOMC_str_list" )
        return self
    def get_depe_label_NOMCSUBJ_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NOMCSUBJ_str_list" )
        return self
    def get_depe_label_NOMCSUBJPASS_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NOMCSUBJPASS_str_list" )
        return self
    def get_depe_label_NUMC_str_list( self ):
        self.functions.insert( 0, "get_depe_label_NUMC_str_list" )
        return self
    def get_depe_label_COP_str_list( self ):
        self.functions.insert( 0, "get_depe_label_COP_str_list" )
        return self
    def get_depe_label_DISLOCATED_str_list( self ):
        self.functions.insert( 0, "get_depe_label_DISLOCATED_str_list" )
        return self



    # text_content #
    def setTextContent( self, text_content ):
        self.text_content = text_content
        return self

    def appendTextContent( self, text_content ):
        self.text_content += text_content
        return self

    def clearTextContent( self ):
        self.text_content = ""
        return self

    # functions #
    def clearFunctions( self ):
        self.functions = []
        return self

    # return_natural_language_raw_data #
    def return_natural_language_raw_data( self, boolean ):
        if boolean :
            self._return_natural_language_raw_data = 1
        else:
            self._return_natural_language_raw_data = 0
        return self

    # natural_language_raw_data #
    def natural_language_raw_data( self, natural_language_raw_data ):
        self._natural_language_raw_data = natural_language_raw_data
        return self

    # build #
    def build( self ):
        json_obj = { "text_content" : self.text_content, "functions": self.functions, "return_natural_language_raw_data": self._return_natural_language_raw_data, "natural_language_raw_data": self._natural_language_raw_data } 
        payload = json.dumps( json_obj )
        return requests.post( self.URL_ENDPOINT, payload )

