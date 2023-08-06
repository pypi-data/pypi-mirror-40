"""
Functions for formatting stuff using ANSI codes and/or esoteric UNICODE characters.
"""

from typing import Union, Iterable, cast

import re
from colorama import Back, Fore, Style
from mhelper import ansi, ansi_helper, exception_helper, string_helper


def format_source( text: str,
                   keywords: Iterable[str],
                   variables: Iterable[str] ) -> str:
    """
    Prints source text, highlighting keywords and variables, and prefixing line numbers
    
    :param text:        Text to print
    :param keywords:    Keywords to highlight
    :param variables:   Variables to highlight
    :return:            Nothing
    """
    r = []
    
    text = text.split( "\n" )
    
    for i, line in enumerate( text ):
        prefix = Back.LIGHTBLACK_EX + Fore.BLACK + " " + str( i ).rjust( 4 ) + " " + Style.RESET_ALL + " "
        
        line = string_helper.highlight_words( line, keywords, Style.RESET_ALL + Fore.GREEN, Style.RESET_ALL )
        line = string_helper.highlight_words( line, variables, Style.RESET_ALL + Fore.CYAN, Style.RESET_ALL )
        
        r.append( prefix + line )
    
    return "\n".join( r )


def format_traceback( exception: Union[BaseException, str],
                      traceback_ = None,
                      warning = False,
                      wordwrap = 0 ) -> str:
    """
    Formats a traceback.
    
    :param exception:       Exception to display 
    :param traceback_:      Traceback text (leave as `None` to get the system traceback) 
    :param warning:         Set to `True` to use warning, rather than error, colours 
    :param wordwrap:        Set to the wordwrap width. 
    :return:                ANSI containing string  
    """
    from mhelper.string_helper import highlight_quotes, highlight_regex
    from mhelper.ansi_helper import cjust, fix_width, wrap
    
    output = []
    wordwrap = wordwrap or 140
    width = wordwrap - 4
    S_V, S_TL, S_H, S_TR, S_VL, S_VR, S_BL, S_BR = "│┌─┐├┤└┘"
    et_col = Style.RESET_ALL + Back.WHITE + (Fore.YELLOW if warning else Fore.RED)  # Error text colour
    eq_col = Style.RESET_ALL + Back.WHITE + Fore.BLACK + ansi.ITALIC  # Error text quotes
    br_col = Fore.WHITE + (Back.YELLOW if warning else Back.RED) # Border colour
    cd_col = Style.RESET_ALL + Back.WHITE + Fore.BLACK  # Code extracts
    fn_col = Style.RESET_ALL + Back.WHITE + Fore.BLUE  # Function name
    ln_col = Style.RESET_ALL + Back.WHITE + Fore.BLUE + ansi.DIM  # File lines
    fi_col = Style.RESET_ALL + Back.WHITE + Fore.BLUE + ansi.BOLD # File names, line numbers
    lb = br_col + S_V + et_col + " "
    rb = et_col + " " + br_col + S_V + Style.RESET_ALL
    
    output.append( br_col + S_TL + S_H * (wordwrap - 2) + S_TR + Style.RESET_ALL )
    
    if not traceback_:
        traceback_ = exception_helper.get_traceback()
    
    lines = traceback_.split( "\n" )
    
    for i, line in enumerate( lines ):
        next_line = lines[i + 2] if i < len( lines ) - 2 else ""
        m = re.search( "Function: (.*)$", next_line )
        if m is not None:
            next_function = m.group( 1 )
        else:
            next_function = None
        
        l = line.strip()
        
        if "Local: " in l:
            l = l.replace( "Local: ", ">" )
            highlight_quotes( l, ">", "=", cd_col, et_col, count = 1 )
            output.append( lb + fix_width( et_col + l, width, justify = 1 ) + rb )
        elif "File " in l or "File: " in l:
            l = ln_col + highlight_regex( l, "\\/([^\\/]*)\"", fi_col, ln_col )
            l = highlight_regex( l, "Line: ([0-9]*);", fi_col, ln_col )
            l = highlight_regex( l, "Function: (.*)$", fi_col, ln_col )
            l = fix_width( l, width )
            output.append( lb + l + rb )
        elif line.startswith( "*" ):
            c = wordwrap - len( l ) - 6
            output.append( br_col + S_VL + cast( str, S_H * 4 ) + l + S_H * c + S_VR + Style.RESET_ALL )
        else:
            l = fix_width( l, width )
            if next_function:
                l = l.replace( next_function, fn_col + next_function + cd_col )
            
            output.append( lb + cd_col + l + rb )
    
    output.append( br_col + S_VL + S_H * (wordwrap - 2) + S_VR + Style.RESET_ALL )
    
    # Exception text
    if isinstance( exception, BaseException ):
        ex = exception
        
        while ex:
            if ex is not exception:
                output.append( lb + cjust( ansi.DIM + ansi.ITALIC + "caused by" + ansi.ITALIC_OFF + ansi.DIM_OFF, width ) + rb )
            
            output.append( lb + (cjust( ansi.UNDERLINE + type( ex ).__name__ + ansi.UNDERLINE_OFF, width ) + rb) )
            ex_text = et_col + highlight_quotes( str( ex ), "«", "»", eq_col, et_col )
            
            for line in wrap( ex_text, width ):
                line = cjust( line, width )
                output.append( lb + line + rb )
            
            ex = ex.__cause__
    
    else:
        output.append( lb + str( exception ).ljust( width ) + rb )
    
    output.append( br_col + S_BL + S_H * (wordwrap - 2) + S_BR + Style.RESET_ALL )
    
    return "\n".join( output )


def format_two_columns( *,
                        left_margin: int,
                        centre_margin: int,
                        right_margin: int,
                        left_text: str,
                        right_text: str,
                        left_prefix: str = "",
                        right_prefix: str = "",
                        left_suffix: str = "",
                        right_suffix: str = "", ):
    """
    Formats a box. 
    :param left_margin:     Width of left margin 
    :param centre_margin:   Width of centre margin 
    :param right_margin:    Width of right margin 
    :param left_text:       Text in left column 
    :param right_text:      Text in right column 
    :param left_prefix:     Text added to left lines
    :param right_prefix:    Text added to right lines
    :param left_suffix:     Text added to left lines
    :param right_suffix:    Text added to right lines
    :return: 
    """
    r = []
    left_space = centre_margin - left_margin - 1
    right_space = right_margin - centre_margin
    
    left_lines = list( left_prefix + x + left_suffix for x in ansi_helper.wrap( left_text, left_space, pad = True ) )
    right_lines = list( right_prefix + x + right_suffix for x in ansi_helper.wrap( right_text, right_space ) )
    num_lines = max( len( left_lines ), len( right_lines ) )
    
    for i in range( num_lines ):
        left = left_lines[i] if i < len( left_lines ) else " " * left_space
        right = right_lines[i] if i < len( right_lines ) else " " * right_space
        
        text = (" " * left_margin) + left + Style.RESET_ALL + " " + right + Style.RESET_ALL
        r.append( text )
    
    return "\n".join( r )
