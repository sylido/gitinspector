[![Latest release](https://img.shields.io/github/release/ejwa/gitinspector.svg?style=flat-square)](https://github.com/ejwa/gitinspector/releases/latest)
[![License](https://img.shields.io/github/license/ejwa/gitinspector.svg?style=flat-square)](https://github.com/ejwa/gitinspector/blob/master/LICENSE.txt)

<h1>
 <img align="left" height="65px"
      src="res/gitinspector_piclet.png"/>
      &nbsp;GitInspector statistical tool
</h1>
<img align="right" width="30%" src="https://raw.github.com/wiki/ejwa/gitinspector/images/html_example.jpg" /> 

GitInspector is a statistical analysis tool which specializes in git repositories. The default analysis shows general statistics per author, which can be complemented with a timeline analysis that shows the contribution density of each author.

This project has forked from Gitinspector by Ejwa Software. This new version drops support for Python 2, cleans up the interface (analyzes all files by default, removes student-specific options, uses more flexibile parseargs util for parsing command line options), and reorganizes the source code. Unfortunately, with this refresh, it was necessary to drop localization support.

Once you have finished reading this page, you can read [How To](docs/HowTo.md) for instructions on getting started and use.

## Feature highlights
  * Compares cumulative work by each author in the history.
  * TODO: Filters results by source language (deduced from file extension)
  * Can display a statistical timeline analysis.
  * Multi-threaded; uses multiple instances of git to speed up analysis when possible.
  * Supports HTML, JSON, XML and plain text output (console).
  * (NEW) TODO: Can calculate lines of code, lines of comments, and lines of whitespace
  * (NEW) Can analyze from different directories within a repository (which allows for more focused breakdowns)

## Example outputs
...

## Language support
A table is given below which describes the various languages, extensions, and comment analysis supported. Note, by default, no file extension will be ignored in the statistical analysis, but more specific results are only available for the languages listed.

| Language                | File extensions              | Comments |
|-------------------------|------------------------------|----------|
| Ada                     | ada, ads, adb                | Yes      |
| C                       | c, h                         | Yes      |
| C++                     | cpp, cc, hpp, hh             | Yes      |
| C#                      | cs                           | Yes      |
| GNU Gettext             | po, pot                      | Yes      |
| Go                      | go                           | Yes      |
| Haskell                 | hs                           | Yes      |
| HTML                    | html, xhtml                  | Yes      |
| Java                    | java                         | Yes      |
| JavaScript              | js                           | Yes      |
| Kotlin                  | kt                           | Yes      |
| LaTeX                   | tex                          | Yes      |
| ML                      | ml, mli                      | Yes      |
| OpenGL Shading Language | glsl, frag, vert, tesc, tese | Yes      |
| Perl                    | pl                           | Yes      |
| PHP                     | php                          | Yes      |
| Python                  | py                           | Yes      |
| Ruby                    | rb                           | Yes      |
| Scala                   | scala                        | Yes      |
| SQL                     | sql                          | Yes      |
| XML                     | xml, jspx                    | Yes      |

If you need support for a language not listed, feel free to add it yourself in `src/languages.py` or request support through a repository issue.

## License
gitinspector is licensed under the *GNU GPL v3*. The gitinspector logo is partly based on the git logo; based on the work of Jason Long. The logo is licensed under the *Creative Commons Attribution 3.0 Unported License*.
