import React from 'react';

const parseAnnotatedText = (text) => {
    const lines = text.split('\n').filter(line => line.trim() !== '');

    return lines.map((line, index) => {
        // Handle bold text (**bold**)
        const boldFormatted = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Handle bullet points (* or +)
        const bulletFormatted = boldFormatted.replace(/^\s*[\*\+]\s*(.*)/, '<li>$1</li>');

        if (bulletFormatted.startsWith('<li>')) {
            return <li key={index} dangerouslySetInnerHTML={{ __html: bulletFormatted }} />;
        }

        // For normal lines
        return <p key={index} dangerouslySetInnerHTML={{ __html: bulletFormatted }} />;
    });
};


const HumanReadableResponse = ({ rawResponse }) => {
    if (!rawResponse) {
        return <p>No response available.</p>;
    }

    const parsedContent = parseAnnotatedText(rawResponse);

    return (
        <div className="p-4 bg-gray-50 rounded-md shadow-md">
            <h2 className="text-xl font-bold mb-4">Human-Like Response</h2>
            <div className="text-base text-gray-800">
                <ul className="list-disc list-inside space-y-2">
                    {parsedContent}
                </ul>
            </div>
        </div>
    );
};

export default HumanReadableResponse;
