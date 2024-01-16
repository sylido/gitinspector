[![Latest release](https://img.shields.io/github/release/ejwa/gitinspector.svg?style=flat-square)](https://github.com/ejwa/gitinspector/releases/latest)
[![License](https://img.shields.io/github/license/ejwa/gitinspector.svg?style=flat-square)](https://github.com/ejwa/gitinspector/blob/master/LICENSE.txt)

<h1>
 <img align="left" height="65px"
      src="https://raw.githubusercontent.com/ejwa/gitinspector/master/gitinspector/html/gitinspector_piclet.png"/>
      &nbsp;GitInspector statistical tool
</h1>
<img align="right" width="30%" src="https://raw.github.com/wiki/ejwa/gitinspector/images/html_example.jpg" /> 

GitInspector is a statistical analysis tool which specializes in git repositories. The default analysis shows general statistics per author, which can be complemented with a timeline analysis that shows the contribution density of each author.

This project has forked from Gitinspector by Ejwa Software.

Once you have finished reading this page, you can read [How To](HowTo.md) for instructions on getting started and use.

## Feature highlights
  * Shows cumulative work by each author in the history.
  * Filters results by source language (deduced from file extension)
  * Can display a statistical timeline analysis.
  * Multi-threaded; uses multiple instances of git to speed up analysis when possible.
  * Supports HTML, JSON, XML and plain text output (console).
  * TODO: Can calculate lines of code, lines of comments, and lines of whitespace
  * TODO: Can report violations of different code metrics.

## Example outputs
...

## Language support
A table is given below which describes the various languages with comment and/or metric support. Note, by default, no file extension will be ignored in the statistical analysis, but more specific results are only available for the languages listed.

| Language                | File extensions              | Comments | Metrics |
|-------------------------|------------------------------|----------|---------|
| Ada                     | ada, ads, adb                | Yes      | No      |
| C                       | c, h                         | Yes      | No      |
| C++                     | cpp, cc, hpp, hh             | Yes      | No      |
| C#                      | cs                           | Yes      | No      |
| GNU Gettext             | po, pot                      | Yes      | No      |
| Go                      | go                           | Yes      | No      |
| Haskell                 | hs                           | Yes      | No      |
| HTML                    | html, xhtml                  | Yes      | No      |
| Java                    | java                         | Yes      | No      |
| JavaScript              | js                           | Yes      | No      |
| Kotlin                  | kt                           | Yes      | No      |
| LaTeX                   | tex                          | Yes      | No      |
| ML                      | ml, mli                      | Yes      | No      |
| OpenGL Shading Language | glsl, frag, vert, tesc, tese | Yes      | No      |
| Perl                    | pl                           | Yes      | No      |
| PHP                     | php                          | Yes      | No      |
| Python                  | py                           | Yes      | No      |
| Ruby                    | rb                           | Yes      | No      |
| Scala                   | scala                        | Yes      | No      |
| SQL                     | sql                          | Yes      | No      |
| XML                     | xml, jspx                    | Yes      | No      |

If you need support for a language not listed, feel free to add it yourself in `src/languages.py` or request support through a repository issue.

## License
gitinspector is licensed under the *GNU GPL v3*. The gitinspector logo is partly based on the git logo; based on the work of Jason Long. The logo is licensed under the *Creative Commons Attribution 3.0 Unported License*.
