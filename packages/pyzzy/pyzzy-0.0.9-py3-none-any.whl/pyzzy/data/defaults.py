import collections
import configparser


__all__ = ["conf", "json_dump", "json_load", "toml", "yaml"]


conf = {
    # Dict data that will be initially put in the DEFAULT section
    #   default:  None
    #   accepted: None, dict
    "defaults": None,
    # Dict factory to use as default for the parser mapping protocol
    #   default:  collections.OrderedDict
    #   accepted: dict-like factory (OrderedDict, dict...)
    "dict_type": collections.OrderedDict,
    # Allow option declaration without both separator and value
    # Value will be set to None on parsing
    #   default:  False
    #   accepted: boolean
    "allow_no_value": False,
    # Substring that delimit keys from values
    #   default:  (": ", ":")
    #   accepted: string or sequence of string
    "delimiters": ("=", ":"),
    # Substring that indicate the beginning of a comment
    #   default:  ("#", ";")
    #   accepted: string or sequence of string
    "comment_prefixes": ("#", ";"),
    # Substring that delimit values from comment
    #   default:  None
    #   accepted: string or sequence of string
    "inline_comment_prefixes": None,
    # In strict mode, duplicates (section or option) are not allowed
    #   default:  True
    #   accepted: boolean
    "strict": True,
    # Allow indented empty lines on multiline values
    #   default:  True
    #   accepted: boolean
    "empty_lines_in_values": True,
    # Name of the section used for defaults
    #   default:  configparser.DEFAULTSECT
    #   accepted: string
    "default_section": configparser.DEFAULTSECT,
    # Class used for interpolation of values
    # default:   configparser.BasicInterpolation()
    # accepted:  configparser.BasicInterpolation()
    #            or configparser.ExtendedInterpolation()
    "interpolation": configparser.BasicInterpolation(),
    # Dict used to create specific converters to be used with getXXX methods
    #   default:  not set (configparser._UNSET = object())
    #   accepted: dict
    # "converters": configparser._UNSET,
}


json_dump = {"indent": 4, "ensure_ascii": False, "default": str}

json_load = {
    "object_hook": collections.OrderedDict,
    "object_pairs_hook": collections.OrderedDict,
}


toml = {"_dict": collections.OrderedDict}


yaml = {
    # Default style for scalars
    #    default:  None
    #    accepted: "", '"', "'", "|", ">"
    "default_style": "",
    # Compact/Minified style with line length < width
    # Not effective with round-trip dumper
    #    default:  None
    #    accepted: boolean
    "default_flow_style": False,
    # Add type tags everywhere (!!str, !!int, !!seq, !!map...)
    #    default:  None
    #    accepted: boolean
    "canonical": False,
    # Number of spaces to use for indentation (new scope)
    #    default:  None (best_indent=2)
    #    accepted: int
    "indent": 4,
    # Number of spaces to use for indentation of dashes in sequences
    #    default:  None
    #    accepted: int
    # "block_seq_indent": 4,
    # Maximum line length
    #    default:  None (best_width=80)
    #    accepted: int
    "width": 55,
    # Allow unicode chars or escape them
    #    default:  None
    #    accepted: boolean
    "allow_unicode": True,
    # Character(s) use for new lines
    # May be forced by 'open' function
    #    default:  None (best_line_break="\n")
    #    accepted: string : "\n", "\r"
    "line_break": "\n",
    # Character encoding
    # May be forced by 'open' function
    # Uneffective with Path-like source
    #    default:  None
    #    accepted: string
    "encoding": "utf-8",
    # Add --- before each document start
    #    default:  None
    #    accepted: boolean
    "explicit_start": True,
    # Add ... after each document end
    #    default:  None
    #    accepted: boolean
    "explicit_end": True,
    # YAML format version "1.1", "1.2" ...
    #    default:  None ("1.2")
    #    accepted: string ("1.1", "1.2")
    # "version": "1.2",
    # Align ":" with 'prefix_colon' for keys at root level
    #    default:  None
    #    accepted: boolean or int
    "top_level_colon_align": False,
    # Character use to align 'top_level_colon'
    #   default:  None
    #   accepted: string
    "prefix_colon": None,
    # Preserve output quotes when input contains quotes
    #    default:  None
    #    accepted: boolean
    "preserve_quotes": True,
    # Allow duplicate keys in map, set
    #    default:  False
    #    accepted: boolean
    "allow_duplicate_keys": False,
    # ???
    #    default:  None
    #    accepted: dict
    "tags": None,
    # ???
    "top_level_block_style_scalar_no_indent_error_1_1": False,
}
