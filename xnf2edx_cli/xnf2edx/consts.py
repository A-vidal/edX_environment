from pathlib import Path

ROOTDIR = Path(__file__).parent.parent
DATA_INPUT = ROOTDIR.joinpath("data", "input")
DATA_OUTPUT = ROOTDIR.joinpath("data", "output")

"""
    CONST DECLARATION
    this consts will help us in case of modifications in the excel sheet
"""

"""
    sheet->tabs
"""
CTABSHEET = "Tabs"
CTABNOMBREROW = 0
CTABCONTENTROW = 1

"""
    sheet->docs
"""
CDOCSHEET = "Docs"
CDOCNOMBREROW = 0
CDOCURLROW = 1

"""
    sheet->conf
"""
CDATOSGENERALESROW = 2
CTTAREAROW = 4
CTTAREASTARTROW = 1
CUNIDADROW = 5
CPROBLEMASROW = 7
CCURSOROW = 6
CSUBROW = 11
CCERTROW = 3
CONFVERSIONPOS = [100, 0]

"""
    sheet->datosgenerales
"""
CDATOSGENERALESSHEET = "DatosGenerales"
CDATOSGENERALESVERSIONPOS = [100, 0]
CDATOSGENERALESNOMBREPOS = [1, 0]
CDATOSGENERALESCATEGORIAPOS = [7, 1]
CDATOSGENERALESEDICIONPOS = [7, 2]
CDATOSGENERALESDISPLAYNAMEPOS = [1, 1]
CDATOSGENERALESSTARTDATEPOS = [1, 2]
CDATOSGENERALESENDDATEPOS = [1, 3]
CDATOSGENERALESINFOPOS = [3, 2]
CDATOSGENERALESABOUTPOS = [3, 4]
CDATOSGENERALESPREREQUISITESPOS = [3, 3]
CDATOSGENERALESTEACHERSPOS = [3, 0]
CDATOSGENERALESEFFORTPOS = [5, 2]
CDATOSGENERALESABOUTVIDEOPOS = [3, 1]
CDATOSGENERALESDURATIONPOS = [5, 1]
# CDATOSGENERALESHANDOUTSPOS = [5, 3]
CDATOSGENERALESPROGRAMPOS = [5, 3]
CDATOSGENERALESEVALPOS = [5, 4]
CDATOSGENERALESVERSION = "0.5"
CDATOSGENERALESPOLICIES = [
    {"coords": [7, 3], "datatype": "bool", "fieldname": "cert_html_view_enabled"},
    {"coords": [7, 4], "datatype": "text", "fieldname": "course_image"},
    {"coords": [9, 1], "datatype": "date", "fieldname": "enrollment_end"},
    {"coords": [9, 2], "datatype": "num", "fieldname": "minimum_grade_credit"},
    {"coords": [9, 3], "datatype": "json", "fieldname": "video_upload_pipeline"},
    {"coords": [9, 4], "datatype": "bool", "fieldname": "mobile_available"},
    {"coords": [11, 1], "datatype": "bool", "fieldname": "self_paced"},
    {"coords": [11, 2], "datatype": "bool", "fieldname": "allow_unsupported_xblocks"},
    {"coords": [11, 3], "datatype": "text", "fieldname": "rerandomize"},
    {"coords": [11, 4], "datatype": "text", "fieldname": "annotation_token_secret"},
    {"coords": [13, 1], "datatype": "text", "fieldname": "matlab_api_key"},
    {"coords": [13, 2], "datatype": "json", "fieldname": "cert_html_view_overrides"},
    {"coords": [13, 3], "datatype": "json", "fieldname": "teams_configuration"},
    {"coords": [13, 4], "datatype": "bool", "fieldname": "create_zendesk_tickets"},
    {"coords": [15, 1], "datatype": "null", "fieldname": "ref"},
    {"coords": [15, 2], "datatype": "bool", "fieldname": "no_grade"},
    {"coords": [15, 3], "datatype": "bool", "fieldname": "is_new"},
    {"coords": [15, 4], "datatype": "text", "fieldname": "catalog_visibility"},
    {"coords": [17, 1], "datatype": "bool", "fieldname": "disable_progress_graph"},
    {"coords": [17, 2], "datatype": "num", "fieldname": "days_early_for_beta"},
    {"coords": [17, 3], "datatype": "text", "fieldname": "enrollment_domain"},
    {"coords": [17, 4], "datatype": "bool", "fieldname": "issue_badges"},
    {"coords": [19, 1], "datatype": "text", "fieldname": "advertised_start"},
    {"coords": [19, 2], "datatype": "text", "fieldname": "due"},
    {"coords": [19, 3], "datatype": "text", "fieldname": "due_date_display_format"},
    {"coords": [19, 4], "datatype": "json", "fieldname": "discussion_blackouts"},
    {"coords": [21, 1], "datatype": "bool", "fieldname": "enable_ccx"},
    {"coords": [21, 2], "datatype": "bool", "fieldname": "allow_proctoring_opt_out"},
    {"coords": [21, 3], "datatype": "bool", "fieldname": "use_latex_compiler"},
    {"coords": [21, 4], "datatype": "bool", "fieldname": "enable_timed_exams"},
    {"coords": [23, 1], "datatype": "bool", "fieldname": "enable_proctored_exams"},
    {"coords": [23, 2], "datatype": "bool", "fieldname": "edxnotes"},
    {"coords": [23, 3], "datatype": "bool", "fieldname": "enable_subsection_gating"},
    {"coords": [23, 4], "datatype": "bool", "fieldname": "video_speed_optimizations"},
    {"coords": [25, 1], "datatype": "text", "fieldname": "course_image"},
    {"coords": [25, 2], "datatype": "json", "fieldname": "learning_info"},
    {"coords": [25, 3], "datatype": "json", "fieldname": "instructor_info"},
    {"coords": [25, 4], "datatype": "null", "fieldname": "ref"},
    {"coords": [27, 1], "datatype": "json", "fieldname": "html_textbooks"},
    {"coords": [27, 2], "datatype": "json", "fieldname": "advanced_modules"},
    {"coords": [27, 3], "datatype": "text", "fieldname": "video_thumbnail_image"},
    {"coords": [27, 4], "datatype": "bool", "fieldname": "show_reset_button"},
    {"coords": [29, 1], "datatype": "bool", "fieldname": "show_calculator"},
    {"coords": [29, 2], "datatype": "text", "fieldname": "showanswer"},
    {"coords": [29, 3], "datatype": "text", "fieldname": "cert_name_short"},
    {"coords": [29, 4], "datatype": "text", "fieldname": "cert_name_long"},
    {"coords": [31, 1], "datatype": "text", "fieldname": "display_organization"},
    {"coords": [31, 2], "datatype": "null", "fieldname": "ref"},
    {"coords": [31, 3], "datatype": "text", "fieldname": "display_name"},
    {
        "coords": [31, 4],
        "datatype": "num",
        "fieldname": "max_student_enrollments_allowed",
    },
    {"coords": [33, 1], "datatype": "num", "fieldname": "max_attempts"},
    {"coords": [33, 2], "datatype": "text", "fieldname": "display_coursenumber"},
    {
        "coords": [33, 3],
        "datatype": "text",
        "fieldname": "certificates_display_behavior",
    },
    {"coords": [33, 4], "datatype": "bool", "fieldname": "discussion_sort_alpha"},
    {"coords": [35, 1], "datatype": "null", "fieldname": "ref"},
    {"coords": [35, 2], "datatype": "bool", "fieldname": "allow_public_wiki_access"},
    {"coords": [35, 3], "datatype": "bool", "fieldname": "allow_anonymous"},
    {"coords": [35, 4], "datatype": "bool", "fieldname": "allow_anonymous_to_peers"},
    {"coords": [37, 1], "datatype": "num", "fieldname": "cosmetic_display_price"},
    {"coords": [37, 2], "datatype": "text", "fieldname": "static_asset_path"},
    {"coords": [37, 3], "datatype": "bool", "fieldname": "invitation_only"},
    {"coords": [37, 4], "datatype": "json", "fieldname": "discussion_topics"},
    {"coords": [39, 1], "datatype": "text", "fieldname": "ccx_connector"},
    {"coords": [39, 2], "datatype": "text", "fieldname": "social_sharing_url"},
    {"coords": [39, 3], "datatype": "text", "fieldname": "annotation_storage_url"},
    {"coords": [39, 4], "datatype": "json", "fieldname": "video_bumper"},
]

CDATOSGENERALESCERTIFICATES = [7, 3]
CDATOSGENERALESIMAGENAME = [7, 4]
CDATOSGENERALESENDREGISTER = [9, 1]
CDATOSGENERALESMINIUMNOTE = [9, 2]
CDATOSGENERALESVIDEOUPLOADID = [9, 3]
CDATOSGENERALESMOBILE = [9, 4]
CDATOSGENERALESSELFPACED = [11, 1]
CDATOSGENERALESUNSUPORTED = [11, 2]
CDATOSGENERALESRANDOMPROBLEMS = [11, 3]
CDATOSGENERALESANNOTATIONSECRET = [11, 4]
CDATOSGENERALESMATLABAPI = [13, 1]
CDATOSGENERALESCONFCERTS = [13, 2]
CDATOSGENERALESCONFTEAM = [13, 3]
CDATOSGENERALESTICKZENDES = [13, 4]
CDATOSGENERALESVIDEOCREDENTIAL = [15, 1]
CDATOSGENERALESNOCALIFIED = [15, 2]
CDATOSGENERALESNEWCOURSE = [15, 3]
CDATOSGENERALESCATALOG = [15, 4]
CDATOSGENERALESPROGRESSDISABLE = [17, 1]
CDATOSGENERALESBETAANTELATION = [17, 2]
CDATOSGENERALESEXTERNALAUTHDOM = [17, 3]
CDATOSGENERALESOPENBADGES = [17, 4]
CDATOSGENERALESPUBLISHEDSTART = [19, 1]
CDATOSGENERALESTASKLIMITDATE = [19, 2]
CDATOSGENERALESTASKLIMITDISPLAY = [19, 3]
CDATOSGENERALESDISCUSIONUNLOCKDATE = [19, 4]
CDATOSGENERALESCCXENABLED = [21, 1]
CDATOSGENERALESNOSUPERVISEDEXAMS = [21, 2]
CDATOSGENERALESLATEXCOMPILER = [21, 3]
CDATOSGENERALESCRONOEXAMS = [21, 4]
CDATOSGENERALESSUPERVISEDEXAMS = [23, 2]
CDATOSGENERALESSTUDENTSNOTE = [23, 2]
CDATOSGENERALESSUBSECTIONPREREQUISITES = [23, 2]
CDATOSGENERALESVIDEOCACHESISTEM = [23, 2]
CDATOSGENERALESABOUTIMAGE = [25, 1]
CDATOSGENERALESLEARNINGINFO = [25, 2]
CDATOSGENERALESINSTRUCTORINFO = [25, 3]
CDATOSGENERALESREMOTEBOOK = [25, 4]
CDATOSGENERALESHTMLTEXTBOOKS = [27, 1]
CDATOSGENERALESADVANCEDMODULES = [27, 2]
CDATOSGENERALESCOURSETHUMBNAIL = [27, 3]
CDATOSGENERALESRESETBUTTON = [27, 4]
CDATOSGENERALESCALCULATOR = [29, 1]
CDATOSGENERALESSHOWANSWER = [29, 2]
CDATOSGENERALESCERTNAMESHORT = [29, 3]
CDATOSGENERALESCERTNAMELARGE = [29, 4]
CDATOSGENERALESORGNAME = [31, 1]
CDATOSGENERALESSTARTTABNAME = [31, 2]
CDATOSGENERALESCOURSEDISPLAYNAME = [31, 3]
CDATOSGENERALESMAXSTUDENTS = [31, 4]
CDATOSGENERALESMAXTRIES = [33, 1]
CDATOSGENERALESDISPLAYNUM = [33, 2]
CDATOSGENERALESCERTPUB = [33, 3]
CDATOSGENERALESORDERDISC = [33, 4]
CDATOSGENERALESLTIPASS = [35, 1]
CDATOSGENERALESPUBLICWIKI = [35, 2]
CDATOSGENERALESANONFORUM = [35, 3]
CDATOSGENERALESANONSTUD = [35, 4]
CDATOSGENERALESCOURSEPRICE = [37, 1]
CDATOSGENERALESSTATICPATH = [37, 2]
CDATOSGENERALESONLYINVITE = [37, 3]
CDATOSGENERALESDISCUSION = [37, 4]
CDATOSGENERALESCCXURL = [39, 1]
CDATOSGENERALESURLSOCIAL = [39, 2]
CDATOSGENERALESURLANOTATIONSTORE = [39, 3]
CDATOSGENERALESVIDEOPREVIOUS = [39, 4]
CDATOSGENERALESSTATICIMPORTPATH = [41, 1]


"""
    sheet->TipodeTarea
"""
CTTAREASHEET = "TipodeTarea"
CTTAREATYPECOL = 0
CTTAREAABREVIATURECOL = 1
CTTAREAWEIGHTCOL = 2
CTTAREADISCARDCOL = 3
CTTAREATRYCOL = 4
CTTAREASHOWANSWERCOL = 5
CTTAREAWEIGHTPROBLEMCOL = 6
CTTAREARANDOMICECOL = 7
CTTAREAAMOUNTCOL = 8

"""
    sheet->unidad
"""
CUNIDADSHEET = "Unidades"
CUNIDADCHAPTERIDCOL = 1
CUNIDADCHAPTERNAMECOL = 2
CUNIDADSUBSECTIONIDCOL = 3
CUNIDADSUBSECTIONNAMECOL = 4
CUNIDADFORMATCOL = 5
CUNIDADSTARTDATECOL = 6
CUNIDADENDDATECOL = 7

"""
    sheet->problemas
"""
CPROBLEMASSHEET = "Problemas"
CPROBLEMASIDUNIDADCOL = 0
CPROBLEMASIDSUBSECCIONCOL = 2
CPROBLEMASIDLECCIONCOL = 4
# TO-DO INTENTOS, MOSTRAR RESPUESTA,PESO Y RANDOMICE
CPROBLEMASINTENTOSCOL = 6
CPROBLEMASSHOWANSWERCOL = 7
CPROBLEMASWEIGHTCOL = 8
CPROBLEMASRANDOMICECOL = 9
CPROBLEMASPREVIACOL = 10
CPROBLEMASTIPOCOL = 11
CPROBLEMASENUNCIADOCOL = 12
CPROBLEMASCOMENTARIOCOL = 13
CPROBLEMASCORRECTACOL = 14
CPROBLEMASRESPUESTACOL = 15

DEFAULTPROBLEMMAXATTEMPTS = "null"
DEFAULTPROBLEMWEIGHT = 1
DEFAULTPROBLEMSHOWANSWER = "finished"

"""
    sheet->leccion
"""
CCURSOSHEET = "Leccion"
CCURSOCHAPTERIDCOL = 0
CCURSOSUBSECTIONIDCOL = 2
CCURSOLESSONIDCOL = 4
CCURSOLESSONDISPLAYNAMECOL = 5
CCURSOOBJETIVOSCOL = 8
CCURSOVIDEOCOL = 9
CCURSORESUMECOL = 11
CCURSOFORUMCOL = 12
CCURSORESETCOL = 15

"""
    sheet->Format
"""
CFORMATSHEET = "TipodeTarea"
CFORMATNAMECOL = 0
CFORMATABBREVIATIONCOL = 1
CFORMATWEIGHTCOL = 2
CFORMATDROPABLECOL = 3
CFORMATMAXATEMPTSCOL = 4
CFORMATSHOWANSWERCOL = 5
CFORMATPROBLEMWEIGHTCOL = 6
CFORMATRANDOMIZECOL = 7

"""
    sheet->Subtitles
"""
CSUBSHEET = "Subtitulos"
CSUBSHEADERROW = 0
CSUBSTARTROW = 1
CSUBVIDEOIDCOL = 0
CSUBSTARTCOL = 1

"""
    sheet->Certificates
"""
CCERTSHEET = "Certificados"
CCERTDESCCOL = 0
CCERTACTIVECOL = 1
CCERTIDCOL = 2
CCERTVERSIONCOL = 3
CCERTNOMCOL = 4
CCERTSIGNNOMCOL = 5
CCERTSIGNIDCOL = 6
CCERTSIGNTITCOL = 7
CCERTSIGNORGCOL = 8
CCERTSIGNPATHCOL = 9



RESETJS = """<script>// <![CDATA[
function reset(){
var xblocks = $("div.vert");

for (i=0;i<xblocks.length;i++)
{
 var locator = $(xblocks[i]).attr("data-id");
var course = $($("div.xblock",$(xblocks[i]))[0]).attr("data-course-id");

 console.log(course);
 var settings = {
      "async": true,
      "crossDomain": true,
      "url": "/courses/" + course + "/xblock/" + locator + "/handler/xmodule_handler/problem_reset",
      "method": "POST",
      "headers": {},
      "data": {}
    }

 $.ajax(settings).done(function (response) {
  location.reload();
 });
}
}
// ]]></script>
  <div class="action">
<div class="problem-action-buttons-wrapper">
    <span class="problem-action-button-wrapper">
        <button type="button" class="reset problem-action-btn btn-default btn-small" onclick="reset();"><span class="icon fa fa-refresh" aria-hidden="true"></span><span aria-hidden="true">Reiniciar</span><span class="sr">Reset your answer</span></button>
    </span>
    </div></div>"""


OKIMG = "<img width ='15' height='15' src='data:image/png;base64,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'/>"

WRONGIMG = "<img width ='15' height='15' src='data:image/png;base64,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'/>"

ENTITIES = [
    ("<br>", "<br/>"),
    ("&lt;", "&#60;"),
    ("&gt;", "&#62;"),
    # ('&delta;', u'\u00e2'),
    # ('&nbsp;', u'&#32;'),
    # ('&acirc;', u'\u00e2'),
    # ('&beta;', u'\u00e2'),
    # ('&lambda;', u'\u00e2'),
    # ('&micro;', u'\u00e2'),
    ("&iquest;", "&#191;"),
    ("&nbsp;", "&#160;"),
    ("&iexcl;", "&#161;"),
    ("&cent;", "&#162;"),
    ("&pound;", "&#163;"),
    ("&curren;", "&#164;"),
    ("&yen;", "&#165;"),
    ("&euro;", "&#8364;"),
    ("&brvbar;", "&#166;"),
    ("&sect;", "&#167;"),
    ("&uml;", "&#168;"),
    ("&copy;", "&#169;"),
    ("&ordf;", "&#170;"),
    ("&laquo;", "&#171;"),
    ("&not;", "&#172;"),
    ("&shy;", "&#173;"),
    ("&reg;", "&#174;"),
    ("&trade;", "&#8482;"),
    ("&macr;", "&#175;"),
    ("&deg;", "&#176;"),
    ("&plusmn;", "&#177;"),
    ("&sup2;", "&#178;"),
    ("&sup3;", "&#179;"),
    ("&acute;", "&#180;"),
    ("&micro;", "&#181;"),
    ("&para;", "&#182;"),
    ("&middot;", "&#183;"),
    ("&cedil;", "&#184;"),
    ("&sup1;", "&#185;"),
    ("&ordm;", "&#186;"),
    ("&raquo;", "&#187;"),
    ("&frac14;", "&#188;"),
    ("&frac12;", "&#189;"),
    ("&frac34;", "&#190;"),
    ("&iquest;", "&#191;"),
    ("&times;", "&#215;"),
    ("&divide;", "&#247;"),
    ("&Agrave;", "&#192;"),
    ("&Aacute;", "&#193;"),
    ("&Acirc;", "&#194;"),
    ("&Atilde;", "&#195;"),
    ("&Auml;", "&#196;"),
    ("&Aring;", "&#197;"),
    ("&AElig;", "&#198;"),
    ("&Ccedil;", "&#199;"),
    ("&Egrave;", "&#200;"),
    ("&Eacute;", "&#201;"),
    ("&Ecirc;", "&#202;"),
    ("&Euml;", "&#203;"),
    ("&Igrave;", "&#204;"),
    ("&Iacute;", "&#205;"),
    ("&Icirc;", "&#206;"),
    ("&Iuml;", "&#207;"),
    ("&ETH;", "&#208;"),
    ("&Ntilde;", "&#209;"),
    ("&Ograve;", "&#210;"),
    ("&Oacute;", "&#211;"),
    ("&Ocirc;", "&#212;"),
    ("&Otilde;", "&#213;"),
    ("&Ouml;", "&#214;"),
    ("&Oslash;", "&#216;"),
    ("&Ugrave;", "&#217;"),
    ("&Uacute;", "&#218;"),
    ("&Ucirc;", "&#219;"),
    ("&Uuml;", "&#220;"),
    ("&Yacute;", "&#221;"),
    ("&THORN;", "&#222;"),
    ("&szlig;", "&#223;"),
    ("&agrave;", "&#224;"),
    ("&aacute;", "&#225;"),
    ("&acirc;", "&#226;"),
    ("&atilde;", "&#227;"),
    ("&auml;", "&#228;"),
    ("&aring;", "&#229;"),
    ("&aelig;", "&#230;"),
    ("&ccedil;", "&#231;"),
    ("&egrave;", "&#232;"),
    ("&eacute;", "&#233;"),
    ("&ecirc;", "&#234;"),
    ("&euml;", "&#235;"),
    ("&igrave;", "&#236;"),
    ("&iacute;", "&#237;"),
    ("&icirc;", "&#238;"),
    ("&iuml;", "&#239;"),
    ("&eth;", "&#240;"),
    ("&ntilde;", "&#241;"),
    ("&ograve;", "&#242;"),
    ("&oacute;", "&#243;"),
    ("&ocirc;", "&#244;"),
    ("&otilde;", "&#245;"),
    ("&ouml;", "&#246;"),
    ("&oslash;", "&#248;"),
    ("&ugrave;", "&#249;"),
    ("&uacute;", "&#250;"),
    ("&ucirc;", "&#251;"),
    ("&uuml;", "&#252;"),
    ("&yacute;", "&#253;"),
    ("&thorn;", "&#254;"),
    ("&yuml;", "&#255;"),
    ("&OElig;", "&#338;"),
    ("&oelig;", "&#339;"),
    ("&Scaron;", "&#352;"),
    ("&scaron;", "&#353;"),
    ("&Yuml;", "&#376;"),
    ("&circ;", "&#710;"),
    ("&tilde", "&#732;"),
    ("&ensp;", "&#8194;"),
    ("&emsp;", "&#8195;"),
    ("&thinsp", "&#8201;"),
    ("&zwnj;", "&8204;"),
    ("&zwj;", "&#8205;"),
    ("&lrm;", "&#8206;"),
    ("&rlm;", "&#8207;"),
    ("&ndash;", "&#8211;"),
    ("&mdash;", "&#8212;"),
    ("&lsquo;", "&#8216;"),
    ("&rsquo;", "&#8217;"),
    ("&sbquo;", "&#8218;"),
    ("&ldquo;", "&#8220;"),
    ("&rdquo;", "&#8221;"),
    ("&bdquo;", "&#8222;"),
    ("&dagger;", "&#8224;"),
    ("&Dagger;", "&#8225;"),
    ("&permil;", "&#8240;"),
    ("&lsaquo;", "&#8249;"),
    ("&rsaquo;", "&#8250;"),
    ("&fnof;", "&#402;"),
    ("&bull;", "&#8226;"),
    ("&hellip;", "&#8230;"),
    ("&prime;", "&#8242;"),
    ("&Prime;", "&#8243;"),
    ("&oline;", "&#8254;"),
    ("&frasl;", "&#8260;"),
    ("&weierp;", "&#8472;"),
    ("&image;", "&#8465;"),
    ("&real;", "&#8476;"),
    ("&alefsym;", "&#8501;"),
    ("&larr;", "&#8592;"),
    ("&uarr;", "&#8593;"),
    ("&rarr;", "&#8594;"),
    ("&darr;", "&#8495;"),
    ("&harr;", "&#8596;"),
    ("&crarr;", "&#8629;"),
    ("&lArr;", "&#8656;"),
    ("&uArr;", "&#8657;"),
    ("&rArr;", "&#8658;"),
    ("&dArr;", "&#8659;"),
    ("&hArr;", "&#8660;"),
    ("&forall;", "&#8704;"),
    ("&part;", "&#8706;"),
    ("&exist;", "&#8707;"),
    ("&empty;", "&#8709;"),
    ("&nabla;", "&#8711;"),
    ("&isin;", "&#8712;"),
    ("&notin;", "&#8713;"),
    ("&ni;", "&#8715;"),
    ("&prod;", "&#8719;"),
    ("&sum;", "&#8721;"),
    ("&minus;", "&#8722;"),
    ("&lowast;", "&#8727;"),
    ("&radic;", "&#8730;"),
    ("&prop;", "&#8733;"),
    ("&infin;", "&#8734;"),
    ("&ang;", "&#8736;"),
    ("&and;", "&#8743;"),
    ("&or;", "&#8744;"),
    ("&cap;", "&#8745;"),
    ("&cup;", "&#8746;"),
    ("&int;", "&#8747;"),
    ("&there4;", "&#8756;"),
    ("&sim;", "&#8764;"),
    ("&cong;", "&#8773;"),
    ("&asymp;", "&#8776;"),
    ("&ne;", "&#8800;"),
    ("&equiv;", "&#8801;"),
    ("&le;", "&#8804;"),
    ("&ge;", "&#8805;"),
    ("&sub;", "&#8834;"),
    ("&sup;", "&#8835;"),
    ("&nsub;", "&#8836;"),
    ("&sube;", "&#8838;"),
    ("&supe;", "&#8839;"),
    ("&oplus;", "&#8853;"),
    ("&otimes;", "&#8855;"),
    ("&perp;", "&#8869;"),
    ("&sdot;", "&#8901;"),
    ("&lceil;", "&#8968;"),
    ("&rceil;", "&#8969;"),
    ("&lfloor;", "&#8970;"),
    ("&rfloor;", "&#8971;"),
    ("&lang;", "&#9001;"),
    ("&rang;", "&#9002;"),
    ("&loz;", "&#9674;"),
    ("&spades;", "&#9824;"),
    ("&clubs;", "&#9827;"),
    ("&hearts;", "&#9829;"),
    ("&diams;", "&#9830;"),
    ("&Alpha;", "&#913;"),
    ("&Beta;", "&#914;"),
    ("&Gamma;", "&#915;"),
    ("&Delta;", "&#916;"),
    ("&Epsilon;", "&#917;"),
    ("&Zeta;", "&#918;"),
    ("&Eta;", "&#919;"),
    ("&Theta;", "&#920;"),
    ("&Iota;", "&#921;"),
    ("&Kappa;", "&#922;"),
    ("&Lambda;", "&#923;"),
    ("&Mu;", "&#924;"),
    ("&Nu;", "&#925;"),
    ("&Xi;", "&#926;"),
    ("&Omicron;", "&#927;"),
    ("&Pi;", "&#928;"),
    ("&Rho;", "&#929;"),
    ("&Sigma;", "&#931;"),
    ("&Tau;", "&#932;"),
    ("&Upsilon;", "&#933;"),
    ("&Phi;", "&#934;"),
    ("&Chi;", "&#935;"),
    ("&Psi;", "&#936;"),
    ("&Omega;", "&#937;"),
    ("&alpha;", "&#945;"),
    ("&beta;", "&#946;"),
    ("&gamma;", "&#947;"),
    ("&delta;", "&#948;"),
    ("&epsilon;", "&#949;"),
    ("&zeta;", "&#950;"),
    ("&eta;", "&#951;"),
    ("&theta;", "&#952;"),
    ("&iota;", "&#953;"),
    ("&kappa;", "&#954;"),
    ("&lambda;", "&#955;"),
    ("&mu;", "&#956;"),
    ("&nu;", "&#957;"),
    ("&xi;", "&#958;"),
    ("&omicron;", "&#959;"),
    ("&pi;", "&#960;"),
    ("&rho;", "&#961;"),
    ("&sigmaf;", "&#962;"),
    ("&sigma;", "&#963;"),
    ("&tau;", "&#964;"),
    ("&upsilon;", "&#965;"),
    ("&phi;", "&#966;"),
    ("&chi;", "&#967;"),
    ("&psi;", "&#968;"),
    ("&omega;", "&#969;"),
    ("&thetasym;", "&#977;"),
    ("&upsih;", "&#978;"),
    ("&piv;", "&#982;"),
]

CONF_SHEET = "conf"

"""
    showanswer
"""
SA_ALWAYS_ROW = 24
SA_ANSWERED_ROW = 25
SA_ATTEMPTED_ROW = 26
SA_CLOSED_ROW = 27
SA_FINISHED_ROW = 28
SA_PASTDATE_ROW = 29
SA_NEVER_ROW = 30

"""
    yesno answers
"""
YES_ROW = 39
NO_ROW = 40
