  // Define the sub-items for each main item
	const subItems = {
    منتجات_البان:
    ["اختار من القائمه ادناه",
    "حليب طازج جاموسي",
    "حليب طازج بقرى",
    "جبنه قريش",
    "جبنه قديمه ",
    "مورته",
    "زبده طازجه بقرىي ",
    "زبده طازجه جاموسي ",
    
    "عسل نحل طبيعى",
    "عسل نحل طبيعى موالح",
    "عسل نحل طبيعى برسيم",
    "عسل نحل طبيعى حبه البركه",
    "عسل نحل طبيعى",
    "زيت زيتون",
    "فطير ",
    "اطباق دجاج طازجه",
    "اطباق بط طازجه",
    "قطعيات لحمه مميزه",
    "عيش بلدى فلاحى"
    ],
    
    فاكهه: 
    ["اختار من القائمه ادناه",
      "برتقال ابو سره",
    "برتقال بلدى",
    "برتقال سكري",
    "يوسفى",
    "ليمون بلدى",
    "تفاح احمر",
    "تفاح اخضر",
    "بلح زغلول",
    "بلح سمانى",
    "بلح رطب",
    "بلح برحى",
    "تين اخضر تركى",
    "تين غامق اسبانى",
    "موز",
    "رمان",
    "مانجو-كيت",
    "مانجو-ناعومي",
    "مانجو - زبديه",
    "بطيخ كبير ",
    "بطيخ وسط",
    "شمام -شهد",
    "كانتلوب",
    "عنب احمر",
    "عنب بناتى",
    "العنب",
    "الزيتون"	
     ],

    خضراوات: 
    ["اختار من القائمه ادناه",
    "جزر",
    "طماطم",
    "بصل احمر & ابيض",
    "توم بلدى",
    "بطاطس تحمير",
    "بطاطا حلوه",
    "بنجر ",
    "خيار ",
    "باميه",
    "فلفل حامى",
    "فلفل رومى اخضر",
    "فلفل الوان",
    "باذنجان رومى",
    "باذنجان ابيض واسود للحشو",
    "كوسه"
     ],

    منتجات_اخرى: 
     ["اختار من القائمه ادناه",
     "جزر",
     "طماطم",
     "بصل احمر ابيض",
     "توم بلدى",
     "بطاطس تحمير",
     "بطاطا حلوه",
     "بنجر ",
     "خيار ",
     "باميه",
     "فلفل حامى",
     "فلفل رومى اخضر",
     "فلفل الوان",
     "باذنجان رومى",
     "باذنجان ابيض واسود للحشو",
     "كوسه"
      ]
 
    };
    
    // Function to populate the sub-dropdown based on the selected main item
    function populateSubDropdown() {
      const mainDropdown = document.getElementById("mainDropdown");
      const subDropdown  = document.getElementById("subDropdown");
      const selectedItem = mainDropdown.value;
      
      // Clear previous options
      subDropdown.innerHTML = "";
      
      // Add new options based on the selected item
      if (selectedItem && subItems[selectedItem]) {
        subItems[selectedItem].forEach(function(subItem) {
          const option = document.createElement("option");
          option.value = subItem;
          option.text = subItem;
          subDropdown.appendChild(option);
        });
      } else {
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "Select a sub-item";
        subDropdown.appendChild(defaultOption);
      }
    }
    
    var outImage ="imagenFondo";
    function preview_2(obj)
    {
      if (FileReader)
      {
        var reader = new FileReader();
        reader.readAsDataURL(obj.files[0]);
        reader.onload = function (e) {
        var image=new Image();
        image.src=e.target.result;
        image.onload = function () {
          document.getElementById(outImage).src=image.src;
        };
        }
      }
      else
      {
            // Not supported
      }
    }
    