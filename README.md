<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a>
    <img src="images/sparql.png" alt="Sparql Logo" width="80" height="80">
  </a>

  <h3 align="center">Sparql Query Parser</h3>

  <p align="center">
    A parser for sparql queries whose output is a Python model of an ingested query.
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project uses recursive descent parsing to build an in-memory Python model of an ingested sparql query. This model can then be modified using method calls, and eventually be converted back to a sparql string. The library could also be used for sparql validation.

While similar projects do exist in the Python ecosystem, I could find none that built a Python model for the developer to play with. SparqlWrapper is a transport library more interested in http details than query building/validation. You must rely on the server-side for validation in this case. While RDFLIB (the parent project to SparqlWrapper) has some great features as well, including an in-memory triple store, it too offers nothing on the query building front.

Here's an example to highlight the usefulness of an in-memory model of a query. Suppose you have an existing Select query. For testing, you decide to select only from a newly created, testing-specific named graph. Without this library, you would be reliant on string manipulation -- searching for keywords, splicing, and inserting. Personally, this feels a code smell to me, but could work. But as the complexity of your query increases, with nested select clauses for instance, string manipulation becomes near-impossible.

The Java ecosystem appears to be well ahead on this front -- I believe Apache Jena has functionality to do what this project accomplishes. Hopefully this will allow Python developers to more fully enter the world of semantic web technologies. 

This library was built according to the Sparql 1.1 documented grammar described here:
https://www.w3.org/TR/sparql11-query/#sparqlGrammar


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Limitations
This was a rushed implementation of the grammar. I did my best to ensure all that was
implemented is accurate and fully tested. However, I had to leave some features out.
I would expect these features to be added easily, should a developer wish to augment
this parsing library. Features left out include:
* Typing using `^^`
* `ConstructQuery`, `DescribeQuery`, `AskQuery`
* `ValuesClause`
* `InlineData`
* `PathNegatedPropertySet`
* `TriplesNodePath`
* `Update`
* Conflation of iriref with '<' or '<='
  - It seems to me an inherent flaw with the sparql grammar. Seems like a double angle bracket ('<<' and '>>') should be used for irirefs. This parser will first attempt to make an iriref, and if not, will turn a '<' or '<=' less than and less than or equal respectively.
  - If you see an iriref created where you don't intend, simply add a whitespace within
  - E.g., which is 7<8&&8>7
    * U_NUMBER_LITERAL, IRIREF, then U_NUMBER_LITERAL (what this library will do)
    * U_NUMBER_LITERAL, LT, U_NUMBER_LITERAL, LOGICAL_AND, U_NUMBER_LITERAL, GT, U_NUMBER_LITERAL



<!-- GETTING STARTED -->
## Getting Started

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing


<!-- LICENSE -->
## License


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->