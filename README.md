# TODO
- Use jQuery for inserting response chunks to execute scripts
- Insert code in <script type="text/chunk"></script> to circumvent javascript escaping?
  Second script loads content of first script (jQuery)
- Remove document.ready script. Could break code that worked before async was used.
  Users who really need this can add this script manually.
  Maybe hosted as static script in this project
