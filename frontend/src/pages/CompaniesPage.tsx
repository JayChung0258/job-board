import React from "react";

const CompaniesPage: React.FC = () => {
  // Mock data for companies
  const companies = [
    { name: "Google", logo: "https://www.google.com/favicon.ico" },
    { name: "Microsoft", logo: "https://www.microsoft.com/favicon.ico" },
    { name: "Apple", logo: "https://www.apple.com/favicon.ico" },
    { name: "Amazon", logo: "https://www.amazon.com/favicon.ico" },
    {
      name: "Meta",
      logo: "https://scontent-fra3-2.xx.fbcdn.net/v/t39.8562-6/256577725_612381820192785_1516860531882870200_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=f537c7&_nc_ohc=Y6H48yyTnTAQ7kNvwFREMA_&_nc_oc=Adn6gCkB14Tktuye-_c-nfc5faKPA-BYw7ftkpZEeXbn4G6-pbFkAw964JNSLdCHvruqnKLEZ8SwtXAaDgXDDS2N&_nc_zt=14&_nc_ht=scontent-fra3-2.xx&_nc_gid=fUtCahYuRUB--5agSVkhJQ&oh=00_AfINyKr1501UJ-Ba1eXCMw8Q1DInyr0vxrVVvw1Tcg8s5w&oe=6831C368",
    },
    { name: "Netflix", logo: "https://www.netflix.com/favicon.ico" },
    { name: "Salesforce", logo: "https://www.salesforce.com/favicon.ico" },
    { name: "Adobe", logo: "https://www.adobe.com/favicon.ico" },
    { name: "Oracle", logo: "https://www.oracle.com/favicon.ico" },
    { name: "IBM", logo: "https://www.ibm.com/favicon.ico" },
    { name: "Intel", logo: "https://www.intel.com/favicon.ico" },
    { name: "Cisco", logo: "https://www.cisco.com/favicon.ico" },
    { name: "SAP", logo: "https://www.sap.com/favicon.ico" },
    { name: "Uber", logo: "https://www.uber.com/favicon.ico" },
    { name: "Twitter", logo: "https://twitter.com/favicon.ico" },
    { name: "Airbnb", logo: "https://www.airbnb.com/favicon.ico" },
    { name: "Spotify", logo: "https://www.spotify.com/favicon.ico" },
    { name: "Slack", logo: "https://slack.com/favicon.ico" },
    { name: "Zoom", logo: "https://zoom.us/favicon.ico" },
    { name: "Dropbox", logo: "https://www.dropbox.com/favicon.ico" },
  ];

  return (
    <div className="w-full bg-gray-50">
      <div className="w-full max-w-[2000px] mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 lg:py-16">
        <div className="text-center mb-12">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            Featured Companies
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Coming soon - We're working on showcasing top tech companies hiring
            now. This section will highlight startups to Fortune 500
            organizations where you can find your next career opportunity.
          </p>
        </div>

        {/* Banner showing work in progress */}
        <div className="mb-10 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-yellow-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                This page is under construction. Company profiles and job
                listings will be available soon.
              </p>
            </div>
          </div>
        </div>

        {/* Company cards grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 sm:gap-6">
          {companies.map((company, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col items-center justify-center p-6 transition-transform duration-300 hover:shadow-md hover:-translate-y-1 cursor-not-allowed opacity-75"
            >
              <div className="w-16 h-16 mb-4 relative flex items-center justify-center">
                <img
                  src={company.logo}
                  alt={`${company.name} logo`}
                  className="max-w-full max-h-full"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.src =
                      "https://via.placeholder.com/32?text=" +
                      company.name.charAt(0);
                  }}
                />
              </div>
              <h3 className="text-lg font-medium text-gray-900 text-center">
                {company.name}
              </h3>
              <span className="text-xs text-gray-500 mt-2 px-2 py-1 bg-gray-100 rounded-full">
                Coming soon
              </span>
            </div>
          ))}
        </div>

        {/* Call to action for companies */}
        <div className="mt-16 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Want to list your company here?
          </h2>
          <button className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out opacity-50 cursor-not-allowed">
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            Register Your Company (Coming Soon)
          </button>
        </div>
      </div>
    </div>
  );
};

export default CompaniesPage;
