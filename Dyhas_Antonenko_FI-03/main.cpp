#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <sstream>
#include <bits/stdc++.h>

using namespace std;

bool valid_char(char c)
{
  bool a1 = ((c <= 122) && (c >= 97));
  bool a2 = ((c <= 90) && (c >= 65));
  bool a3 = ((c <= 57) && (c >= 48));
  bool a4 = (c == '_');

  return a1 || a2 || a3 || a4;
}

string next_word(istream& str)
{
  string result;
  char c;

  while (str.peek() != EOF && !valid_char(str.peek())) 
  {
    if(!str.get(c)) {break;}
  }

  while (str.peek() != EOF)
  {
    if(!valid_char(str.peek())) {return result;}
    else 
    {
      str.get(c);
      result.push_back(c);
    }
  }

  return result;
}

class Collection
{
public:
  Collection(string n = "") : name{n} {};

  string name;
  vector<string> coll;
  map<string, map<int, vector<int>>> index;

  void insert(string text)
  {
    stringstream str(text);

    int i = 0;
    while (true)
    {
      string w = next_word(str);

      if(w == "") {break;}
      else 
      {
        (index[w])[coll.size()].push_back(i);
        i++;
      }
    }

    coll.push_back(text);

    cout << "The document was inserted into " << name << " as d" << coll.size() - 1 << '.' << endl << endl;
  }
  
  void print_index()
  {
    for(auto t = index.begin(); t != index.end(); ++t)
    {
      cout << '\"' << t->first << "\":" << endl;

      for(auto k = t->second.begin(); k != t->second.end(); ++k)
      {
        cout << "   d" << k->first << " -> [";

        for (int i = 0; i < k->second.size() - 1; i++)
        {
          cout << k->second[i] << ", ";
        } 
        cout << k->second[k->second.size() - 1] << "];" << endl;
      }
    }
    cout << endl;
  }

  void search(string where_keyword)
  {
    if (coll.size() == 0) {cout << "The collection is empty." << endl << endl; }
    else if (where_keyword == "")
    {
      cout << "All documents:" << endl;

      int t = 0;
      cout << "[d" << t;
      t++;

      for( ; t < coll.size(); t++)
      {
        cout << ", " << 'd' << t;
      }
      cout << ']';
    }
    else if (index.count(where_keyword) != 0)
    {
      cout << '\"' << where_keyword << "\" :" << endl;

      auto t = index[where_keyword].begin();
      cout << "[d" << t->first;
      ++t;

      for(; t != index[where_keyword].end(); ++t)
      {
        cout << ", " << 'd' << t->first;
      }
      cout << ']';
    }
    else {cout << "There is no such keyword in the collection.";}

    cout << endl << endl;
  }

};

string next_command_token()
{
  string result;
  char c;

  while(isspace(cin.peek())) {cin.get(c);}

  if(cin.peek() == ';') 
  {
    cin.get();
    return ";";
  }

  while(valid_char(cin.peek()))
  {
    cin.get(c);
    result.push_back(c);
  }

  return result;
}

string to_lower(string a)
{
  string temp = a;
  transform(temp.begin(), temp.end(), temp.begin(), ::tolower);
  return temp;
}

map<string, Collection> database;

int execute_command()
{
  string cmd1 = next_command_token();

    if(to_lower(cmd1) == "exit" || to_lower(cmd1) == "\nexit") 
    {
      string end = next_command_token();

      if(end == ";") {return 1;}
      else 
      {
        string terminate;
        getline(cin, terminate, ';');
        cout << "Unknow command \"" << cmd1 << end << "\"." << endl; 
        return 0;
      }
    }

    if(to_lower(cmd1) == "create")
    {
      string name = next_command_token();

      if(name == "") 
      {
        char symb;
        cin.get(symb);
        string terminate;
        getline(cin, terminate, ';');
        cout << "Unexpected symbol \'" << symb << "\'." << endl; return 0;
      }
      else
      {
        string end = next_command_token();

        if(end != ";") 
        {
          string terminate;
          getline(cin, terminate, ';');
          cout << "Expected closing \';\' instead of \"" << terminate << "\"." << endl; 
          return 0;
        }
        else
        {
          database[name].name = name;
          cout << "Succesfully created collection \"" << name << "\"." << endl << endl; 
          return 0;
        }
      }
    }
    else if(to_lower(cmd1) == "insert")
    {
      string name = next_command_token();

      if(name == "") 
      {
        string terminate;
        getline(cin, terminate, ';');
        cout << "Unexpected symbol ->\'" << terminate << "\'." << endl; return 0;
      }
      else
      {
        string next = next_command_token();

        if(next != "") 
        {
          if(next != ";")
          {
            string terminate;
            getline(cin, terminate, ';');
          }
          cout << "Unexpected symbol \'" << next << "\'." << endl; 
          return 0;
        }

        if(cin.peek() != '\"') 
        {
          string terminate;
          getline(cin, terminate, ';');
          cout << "Unexpected symbol ->\'" << terminate << "\'." << endl; 
          return 0;
        }

        string text;

        getline(cin, text, ';');
        
        auto t = text.end() - 1;
        while (isspace(*t)) {--t;}

        if(*t != '\"') {cout << "Expected closing \" before ;" << endl; return 0;}

        if (database[name].name == "") {database[name].name = name;}

        database[name].insert(text.substr(1,text.length() - 2));
      }
    }
    else if(to_lower(cmd1) == "print_index")
    {
      string name = next_command_token();

      if(name == "") 
      {
        string terminate;
        getline(cin, terminate, ';');
        cout << "Unexpected symbol \'" << terminate << "\'." << endl; return 0;
      }
      else
      {
        string end = next_command_token();

        if(end != ";") 
        {
          string terminate;
          getline(cin, terminate, ';');
          cout << "Expected closing \';\' instead of ->\"" << terminate << "\"." << endl; 
          return 0;
        }
        else
        {
          database[name].print_index();
          return 0;
        }
      }
    }
    else if(to_lower(cmd1) == "search")
    {
      string name = next_command_token();

      if(name == "") 
      {
        string terminate;
        getline(cin, terminate, ';');
        cout << "Unexpected symbol ->\'" << terminate << "\'." << endl; return 0;
      }
      else
      {
        if(database.count(name) == 0)
        {
          string terminate;
          getline(cin, terminate, ';');
          cout << "Collection \"" << name << "\" does not exist." << endl;
          return 0;
        }

        string where = next_command_token();

        if(where == ";") 
        {
          database[name].search("");
          return 0;
        }
        else if(to_lower(where) == "where")
        {
          string next = next_command_token();

          if(next != "") 
          {
            if(next != ";")
            {
              string terminate;
              getline(cin, terminate, ';');
            }

            cout << "Unexpected symbol \'" << next << "\'." << endl; 
            return 0;
          }

          if(cin.peek() != '\"') {cout << "Unexpected symbol \'" << cin.peek() << "\'." << endl; return 0;}

          string text;

          getline(cin, text, ';');

          if(*(text.end() - 1) != '\"') {cout << "Expected closing \" before ;" << endl; return 0;}

          database[name].search(text.substr(1,text.length() - 2));
        } 
        else 
        {
          string terminate;
          getline(cin, terminate, ';');
          cout << "Unexpected symbol ->\'" << where << "\'." << endl; 
          return 0;
        }
      }
    }
    else
    {
      string terminate;
      getline(cin, terminate, ';');
      cout << "Unknow command \"" << cmd1 << "\"." << endl; 
      return 0;
    }

    return 0;
}

int main()
{
  while (true)
  {
    if(execute_command() == 1) {return 0;}
  }
}